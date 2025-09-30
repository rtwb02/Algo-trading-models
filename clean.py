"""
Reusable data cleaning utilities (abstracted).

Demonstrates:
Type coercion for dates and numerics
Handling missing values with strategies
Duplicate removal and column trimming
Simple validation checks

This module avoids domain-specific formulas and retains safe placeholders.
"""

import pandas as pd
from typing import List, Optional

def coercedates(df: pd.DataFrame, datecols: List[str]) -> pd.DataFrame:
    for col in datecols:
        if col in df.columns:
            df[col] = pd.todatetime(df[col], errors="coerce")
    return df

def coercenumerics(df: pd.DataFrame, numericcols: List[str]) -> pd.DataFrame:
    for col in numericcols:
        if col in df.columns:
            df[col] = pd.tonumeric(df[col], errors="coerce")
    return df

def dropduplicatesandtrim(df: pd.DataFrame, subset: Optional[List[str]] = None) -> pd.DataFrame:
    df = df.dropduplicates(subset=subset).copy()
    df = df.dropna(how="all").resetindex(drop=True)
    return df

def handlemissing(df: pd.DataFrame, strategy: str = "median", cols: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Simple missing handling strategy:
    - 'median': fill numeric with column median
    - 'mean': fill numeric with column mean
    - 'zero': fill numeric with 0
    - 'ffill': forward fill (time-series)
    """
    if cols is None:
        cols = [c for c in df.columns if pd.api.types.isnumericdtype(df[c])]
    for col in cols:
        if strategy == "median":
            df[col] = df[col].fillna(df[col].median())
        elif strategy == "mean":
            df[col] = df[col].fillna(df[col].mean())
        elif strategy == "zero":
            df[col] = df[col].fillna(0)
        elif strategy == "ffill":
            df[col] = df[col].ffill()
    return df

def validatecolumns(df: pd.DataFrame, requiredcols: List[str]) -> bool:
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        print(f"[?][?] Missing required columns: {missing}")
        return False
    return True
