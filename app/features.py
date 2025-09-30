from __future__ import annotations
from typing import List, Tuple
import pandas as pd


BASE_WEATHER_FEATURES: Tuple[str, ...] = (
    "precipitation_sum",
    "rain_sum",
    "precipitation_hours",
    "temperature_2m_max",
    "temperature_2m_min",
    "wind_speed_10m_max",
    "shortwave_radiation_sum",
)


def base_weather_columns() -> List[str]:
    return list(BASE_WEATHER_FEATURES)


def add_weather_rollups(df: pd.DataFrame, windows: Tuple[int, ...] = (3, 7, 14, 30)) -> pd.DataFrame:
    out = df.copy()
    for c in base_weather_columns():
        if c in out.columns:
            out[f"{c}_lag1"] = out[c].shift(1)
            for w in windows:
                minp = max(2, w // 2)
                out[f"{c}_rmean_{w}"] = out[c].shift(1).rolling(w, min_periods=minp).mean()
                out[f"{c}_rstd_{w}"] = out[c].shift(1).rolling(w, min_periods=minp).std()
    return out
