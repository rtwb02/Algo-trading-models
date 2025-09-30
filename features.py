"""
Feature engineering showcase with abstracted formulas.

Demonstrates:
Date parsing, sorting
Lag features
Rolling-window computations
Groupby-based aggregates
Weekly summaries
Safe placeholders for proprietary formulas
"""

import os
import numpy as np
import pandas as pd
from typing import List
from .config import (
    CURRENTDIR, CURRENTPROCESSEDSUFFIX
)

def addlagfeatures(df: pd.DataFrame, cols: List[str], lag: int = 1) -> pd.DataFrame:
    for c in cols:
        if c in df.columns:
            df[f"{c}Lag{lag}"] = df[c].shift(lag)
    return df

def calculatecustomindicator(df: pd.DataFrame, period: int = 7) -> pd.Series:
    """
    Example of a rolling-window indicator calculation.
    Core formula intentionally abstracted.
    """
    # Placeholder Series with correct index and name
    return pd.Series(np.nan, index=df.index, name="CustomIndicator")

def processcurrentfiles():
    """
    Reads current files, applies abstracted feature engineering,
    and saves processed outputs per dataset.
    """
    currentfiles = [f for f in os.listdir(CURRENTDIR) if f.endswith(".csv")]
    if not currentfiles:
        print("No current files found. Skipping.")
        return

    for file in currentfiles:
        basename = file.replace(".csv", "")
        path = os.path.join(CURRENTDIR, file)

        try:
            df = pd.readcsv(path)

            # Date handling and sorting
            if "Date" in df.columns:
                df["Date"] = pd.todatetime(df["Date"], errors="coerce")
                df = df.sortvalues("Date").resetindex(drop=True)

            # Abstracted engineered columns (placeholders)
            if set(["Open", "Close"]).issubset(df.columns):
                df["DailyPct"] = np.nan  # placeholder
            if set(["High", "Low", "Open"]).issubset(df.columns):
                df["TR"] = np.nan         # placeholder
                df["ATR7"] = np.nan      # placeholder

            # Consecutive run length (abstracted)
            if "DailyPct" in df.columns:
                df["DayPositive"] = np.where(df["DailyPct"] > 0, 1, 0)
                grp = (df["DayPositive"] != df["DayPositive"].shift(1)).cumsum()
                df["ConsecutivePosNegDays"] = df.groupby(grp).cumcount() + 1

            # Open-to-extrema percentages (abstracted)
            df["OpentoHighPct"] = np.nan
            df["OpentoLowPct"] = np.nan

            # Lag features
            lagsourcecols = ["DailyPct", "TR", "ATR7", "DayPositive",
                               "ConsecutivePosNegDays", "OpentoHighPct", "OpentoLowPct"]
            df = addlagfeatures(df, lagsourcecols, lag=1)

            # Time features
            if "Date" in df.columns:
                iso = df["Date"].dt.isocalendar()
                df["Year"] = iso.year
                df["Week"] = iso.week
                df["DayOfWeek"] = df["Date"].dt.dayname()

            # Weekly aggregates (placeholders)
            df["VWAPWeekly"] = np.nan
            df["DistOpenVWAPpct"] = np.nan

            # Gap features (abstracted)
            df["PreviousClose"] = df["Close"].shift(1) if "Close" in df.columns else np.nan
            df["OPG"] = np.nan

            # Custom indicator
            df["CustomIndicator"] = calculatecustomindicator(df, period=7)
            df["CustomIndicatorDiff"] = df["CustomIndicator"] - df["CustomIndicator"].shift(1)

            # Clean up example
            for c in ["Year", "Week"]:
                if c in df.columns:
                    df.drop(columns=[c], inplace=True)

            df = df.dropna(how="all").resetindex(drop=True)

            # Save processed file
            outfile = os.path.join(CURRENTDIR, f"{basename}{CURRENTPROCESSEDSUFFIX}")
            df.tocsv(outfile, index=False)
            print(f"Created processed file: {outfile}")

        except Exception as e:
            print(f"Error processing {basename}: {e}")

def main():
    processcurrentfiles()

if name == "main":
    main()
