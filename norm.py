"""
Normalization pipeline for structured data with abstracted feature names.

Demonstrates:
Fitting a scaler on training data
Applying transformations to current data
Preserving original columns before normalization
Saving normalized outputs
"""

import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from .config import (
    SPLITDIR, CURRENTDIR, NORMALIZEDDIR,
    TRAINSUFFIX, CURRENTPROCESSEDSUFFIX, CURRENTNORMSUFFIX,
    NORMALIZECOLS
)

def normalizecurrentagainsttrain():
    trainfiles = [f for f in os.listdir(SPLITDIR) if f.endswith(TRAINSUFFIX)]

    for file in trainfiles:
        basename = file.replace(TRAINSUFFIX, "")
        trainpath = os.path.join(SPLITDIR, f"{basename}{TRAINSUFFIX}")
        currentpath = os.path.join(CURRENTDIR, f"{basename}{CURRENTPROCESSEDSUFFIX}")
        if not os.path.exists(currentpath):
            print(f"[?][?] No current processed file for {basename}")
            continue

        dftrain = pd.readcsv(trainpath)
        availablecolstrain = [c for c in NORMALIZECOLS if c in dftrain.columns]
        if not availablecolstrain:
            print(f"[?][?] Skipping {basename}: no normalizable columns in train.")
            continue

        scaler = MinMaxScaler()
        scaler.fit(dftrain[availablecolstrain])

        dfcurrent = pd.readcsv(currentpath)
        availablecolscurrent = [c for c in availablecolstrain if c in dfcurrent.columns]
        if not availablecolscurrent:
            print(f"[?][?] Skipping {basename}: no overlapping normalization columns in current.")
            continue

        # Preserve a few originals before normalization
        for col in availablecolscurrent[:3]:
            dfcurrent[f"{col}Orig"] = dfcurrent[col]

        dfcurrent[availablecolscurrent] = scaler.transform(dfcurrent[availablecolscurrent])
        outpath = os.path.join(NORMALIZEDDIR, f"{basename}{CURRENTNORMSUFFIX}")
        dfcurrent.tocsv(outpath, index=False)
        print(f" Saved normalized current: {outpath}")

    print(" All current datasets normalized and saved.")

def main():
    normalizecurrentagainsttrain()

if name == "main":
    main()
