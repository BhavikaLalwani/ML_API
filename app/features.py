from __future__ import annotations
from typing import List, Tuple
import pandas as pd


# Base weather features matching your package exactly
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
    """Return the base numeric columns used before rollups, matching the notebook."""
    return list(BASE_WEATHER_FEATURES)


def add_weather_rollups(df: pd.DataFrame, windows: Tuple[int, ...] = (3, 7, 14, 30)) -> pd.DataFrame:
    """Add lag1, rolling mean and std for base weather columns using past-only windows."""
    out = df.copy()
    for c in base_weather_columns():
        if c in out.columns:
            out[f"{c}_lag1"] = out[c].shift(1)
            for w in windows:
                minp = max(2, w // 2)
                out[f"{c}_rmean_{w}"] = out[c].shift(1).rolling(w, min_periods=minp).mean()
                out[f"{c}_rstd_{w}"] = out[c].shift(1).rolling(w, min_periods=minp).std()
    return out
