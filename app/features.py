import pandas as pd
from typing import List, Tuple


def base_weather_columns() -> List[str]:
    """Return the base weather columns expected by the model."""
    return [
        "temperature_2m_max", "temperature_2m_min",
        "precipitation_sum", "rain_sum", "showers_sum",
        "snowfall_sum", "precipitation_hours",
        "wind_speed_10m_max", "wind_gusts_10m_max",
        "shortwave_radiation_sum", "et0_fao_evapotranspiration",
    ]


def add_weather_rollups(df: pd.DataFrame, windows: Tuple[int, ...] = (3, 7, 14, 30)) -> pd.DataFrame:
    """Add rolling window features to weather data."""
    df = df.copy()
    
    # Sort by date to ensure proper rolling calculations
    if 'date' in df.columns:
        df = df.sort_values('date').reset_index(drop=True)
    
    # Add rolling features for each window
    for window in windows:
        for col in base_weather_columns():
            if col in df.columns:
                # Add rolling mean
                df[f"{col}_mean_{window}d"] = df[col].rolling(window=window, min_periods=1).mean()
                
                # Add rolling sum for precipitation-related columns
                if any(precip in col.lower() for precip in ['precipitation', 'rain', 'snow']):
                    df[f"{col}_sum_{window}d"] = df[col].rolling(window=window, min_periods=1).sum()
                
                # Add rolling max for temperature and wind
                if any(temp_wind in col.lower() for temp_wind in ['temperature', 'wind']):
                    df[f"{col}_max_{window}d"] = df[col].rolling(window=window, min_periods=1).max()
                
                # Add rolling min for temperature
                if 'temperature' in col.lower():
                    df[f"{col}_min_{window}d"] = df[col].rolling(window=window, min_periods=1).min()
    
    return df
