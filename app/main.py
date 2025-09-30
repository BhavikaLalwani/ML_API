from __future__ import annotations
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import List

import joblib
import pandas as pd
import requests
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse


from app.features import add_weather_rollups, base_weather_columns

LAT = -33.8678
LON = 151.2073
ERA5_BASE = "https://archive-api.open-meteo.com/v1/era5"

DAILY_VARS: List[str] = [
    "temperature_2m_max","temperature_2m_min",
    "precipitation_sum","rain_sum","showers_sum",
    "snowfall_sum","precipitation_hours",
    "wind_speed_10m_max","wind_gusts_10m_max",
    "shortwave_radiation_sum","et0_fao_evapotranspiration",
]

BASE_DIR = Path(__file__).parent
MODELS_DIR = BASE_DIR / "models"
RAIN_MODEL_PATH = MODELS_DIR / "rain_or_not" / "rf_clf.joblib"
PRECIP_MODEL_PATH = MODELS_DIR / "precipitation_fall" / "rf_reg.joblib"

app = FastAPI(title="Open Meteo Prediction API")


def _parse_date(s: str) -> date:
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")


def _resolve_model_path(preferred: Path) -> Path:
    if preferred.exists():
        return preferred
    alt = preferred.with_suffix(".pkl")
    if alt.exists():
        return alt
    raise HTTPException(status_code=500, detail=f"Model not found (.joblib/.pkl) at {preferred} or {alt}")


def _load_model(path: Path):
    path = _resolve_model_path(path)
    try:
        return joblib.load(path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load model: {e}")


def _fetch_daily_range(start: date, end: date) -> pd.DataFrame:
    params = {
        "latitude": LAT,
        "longitude": LON,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "daily": ",".join(DAILY_VARS),
        "timezone": "Australia/Sydney",
    }
    r = requests.get(ERA5_BASE, params=params, timeout=60)
    if r.status_code != 200:
        raise HTTPException(status_code=502, detail=f"Upstream error: {r.text[:200]}")
    j = r.json()
    daily = j.get("daily")
    if not daily or "time" not in daily:
        raise HTTPException(status_code=502, detail="Unexpected response schema from Open-Meteo")
    df = pd.DataFrame(daily)
    df["time"] = pd.to_datetime(df["time"])
    df = df.rename(columns={"time": "date"}).sort_values("date").reset_index(drop=True)
    return df


def _build_latest_feature_row(ref_date: date) -> pd.DataFrame:
    start = ref_date - timedelta(days=60)
    end = ref_date
    df = _fetch_daily_range(start, end)

    missing = [c for c in base_weather_columns() if c not in df.columns]
    if missing:
        raise HTTPException(status_code=500, detail=f"Missing required columns from API: {missing}")

    feat = add_weather_rollups(df, windows=(3, 7, 14, 30))
    feat = feat.dropna().reset_index(drop=True)
    if feat.empty:
        raise HTTPException(status_code=500, detail="Insufficient history to build features")
    x = feat.tail(1).copy()
    return x


@app.get("/")
def root() -> JSONResponse:
    return JSONResponse({
        "project": "Open Meteo: Rain (7d) and Precipitation (3d) Prediction API",
        "endpoints": [
            "/", "/health/", "/predict/rain/", "/predict/precipitation/fall/"
        ],
        "inputs": {
            "/predict/rain/": {"date": "YYYY-MM-DD"},
            "/predict/precipitation/fall/": {"date": "YYYY-MM-DD"},
        },
        "outputs": {
            "/predict/rain/": {
                "input_date": "YYYY-MM-DD",
                "prediction": {"date": "YYYY-MM-DD", "will_rain": True}
            },
            "/predict/precipitation/fall/": {
                "input_date": "YYYY-MM-DD",
                "prediction": {"start_date": "YYYY-MM-DD", "end_date": "YYYY-MM-DD", "precipitation_fall": 28.2}
            }
        },
        "github": "https://github.com/BhavikaLalwani/ML_API",
    })


@app.get("/health/")
def health() -> JSONResponse:
    return JSONResponse({"status": "ok", "message": "Open Meteo API healthy"})


@app.get("/predict/rain/")
def predict_rain(date: str = Query(..., description="YYYY-MM-DD")) -> JSONResponse:
    input_date = _parse_date(date)
    target_date = input_date + timedelta(days=7)

    X = _build_latest_feature_row(input_date)
    model = _load_model(RAIN_MODEL_PATH)

    if hasattr(model, "feature_names_in_"):
        cols = list(model.feature_names_in_)
        for c in cols:
            if c not in X.columns:
                X[c] = 0.0
        X = X[cols]

    try:
        proba = float(model.predict_proba(X)[:, 1][0]) if hasattr(model, "predict_proba") else float(model.predict(X)[0])
        will_rain = bool(proba >= 0.5) if 0.0 <= proba <= 1.0 else bool(model.predict(X)[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

    return JSONResponse({
        "input_date": input_date.isoformat(),
        "prediction": {"date": target_date.isoformat(), "will_rain": will_rain},
    })


@app.get("/predict/precipitation/fall/")
def predict_precipitation_fall(date: str = Query(..., description="YYYY-MM-DD")) -> JSONResponse:
    input_date = _parse_date(date)
    start_date = input_date + timedelta(days=1)
    end_date = input_date + timedelta(days=3)

    X = _build_latest_feature_row(input_date)
    model = _load_model(PRECIP_MODEL_PATH)

    if hasattr(model, "feature_names_in_"):
        cols = list(model.feature_names_in_)
        for c in cols:
            if c not in X.columns:
                X[c] = 0.0
        X = X[cols]

    try:
        pred_mm = float(model.predict(X)[0])
        if pred_mm < 0:
            pred_mm = 0.0
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

    return JSONResponse({
        "input_date": input_date.isoformat(),
        "prediction": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "precipitation_fall": round(pred_mm, 2),
        },
    })


