"""
Automated model training & evaluation pipeline (abstracted).

Demonstrates:
Iterating over datasets
Candidate feature discovery via patterns
Logistic regression training and evaluation
Feature subset search (combinatorial, bounded)
Saving predictions and final summary

All feature names and target are abstracted to avoid leaking proprietary logic.
"""

import os
import itertools
import pandas as pd
from typing import List
from sklearn.linearmodel import LogisticRegression
from sklearn.metrics import accuracyscore, classificationreport

from .config import (
    NORMALIZEDDIR, PREDICTIONSDIR,
    TRAINSUFFIX, TESTSUFFIX, CURRENTNORMSUFFIX,
    TARGETCOL, EXCLUDEFEATURES,
    CANDIDATEFEATUREPREFIXES, LAGSUFFIX
)

def discovercandidatefeatures(columns: List[str]) -> List[str]:
    """
    Returns features that match abstracted prefixes or lag suffix patterns,
    excluding known non-feature columns.
    """
    candidates = []
    for col in columns:
        if col in EXCLUDEFEATURES:
            continue
        if col.endswith(LAGSUFFIX):
            candidates.append(col)
            continue
        if any(col.startswith(prefix) for prefix in CANDIDATEFEATUREPREFIXES):
            candidates.append(col)
            continue
    return candidates

def trainandselectfeatures(dftrain: pd.DataFrame, dftest: pd.DataFrame, candidatefeatures: List[str]):
    """
    Try combinations of features and return the best model and feature set.
    Combinatorial search is intentionally bounded for demo purposes.
    """
    bestaccuracy = 0.0
    bestfeatures = []
    bestmodel = None
    bestreporttest = None

    for r in range(2, min(6, len(candidatefeatures) + 1)):
        for combo in itertools.combinations(candidatefeatures, r):
            features = list(combo)
            if not all(f in dftrain.columns for f in features):
                continue
            if not all(f in dftest.columns for f in features):
                continue

            Xtrain = dftrain[features]
            ytrain = dftrain[TARGETCOL]
            Xtest = dftest[features]
            ytest = dftest[TARGETCOL]

            model = LogisticRegression(maxiter=5000)
            model.fit(Xtrain, ytrain)
            ypred = model.predict(Xtest)
            acc = accuracyscore(ytest, ypred)

            if acc > bestaccuracy:
                bestaccuracy = acc
                bestfeatures = features
                bestmodel = model
                bestreporttest = classificationreport(ytest, ypred, outputdict=True)

    return bestmodel, bestfeatures, bestreporttest

def runpredictions():
    trainfiles = [f for f in os.listdir(NORMALIZEDDIR) if f.endswith(TRAINSUFFIX)]
    summaryresults = []

    currentfiles = {
        f.replace(CURRENTNORMSUFFIX, ""): os.path.join(NORMALIZEDDIR, f)
        for f in os.listdir(NORMALIZEDDIR) if f.endswith(CURRENTNORMSUFFIX)
    }

    for trainfile in trainfiles:
        basename = trainfile.replace(TRAINSUFFIX, "")
        testfile = basename + TESTSUFFIX
        trainpath = os.path.join(NORMALIZEDDIR, trainfile)
        testpath = os.path.join(NORMALIZEDDIR, testfile)
        currentpath = currentfiles.get(basename)

        if not os.path.exists(testpath):
            print(f"[?][?] Missing test file for {basename}. Skipping...")
            continue

        dftrain = pd.readcsv(trainpath)
        dftest = pd.readcsv(testpath)
        dfcurrent = pd.readcsv(currentpath) if currentpath and os.path.exists(currentpath) else None

        if TARGETCOL not in dftrain.columns or TARGETCOL not in dftest.columns:
            print(f"Target column '{TARGETCOL}' missing for {basename}. Skipping...")
            continue

        candidatefeatures = discovercandidatefeatures(dftrain.columns)
        if not candidatefeatures:
            print(f"No candidate features for {basename}. Skipping...")
            continue

        print(f"\n Evaluating feature combinations for {basename}...")
        bestmodel, bestfeatures, bestreporttest = trainandselectfeatures(dftrain, dftest, candidatefeatures)

        if bestmodel is None:
            print(f" No valid feature combinations found for {basename}.")
            continue

        # Save test predictions
        dftest["Pred"] = bestmodel.predict(dftest[bestfeatures])
        testout = os.path.join(PREDICTIONSDIR, f"{basename}TestPred.csv")
        dftest.tocsv(testout, index=False)
        print(f" Saved test predictions: {testout}")

        # Predict on current data if available
        if dfcurrent is not None and all(f in dfcurrent.columns for f in bestfeatures):
            dfcurrent["Pred"] = bestmodel.predict(dfcurrent[bestfeatures])
            currout = os.path.join(PREDICTIONSDIR, f"{basename}CurrentPred.csv")
            dfcurrent.tocsv(currout, index=False)
            print(f" Saved current predictions: {currout}")

            # Optional evaluation if TARGETCOL exists in current
            if TARGETCOL in dfcurrent.columns:
                ycurrent = dfcurrent[TARGETCOL]
                ypredcurrent = dfcurrent["Pred"]
                reportcurrent = classificationreport(ycurrent, ypredcurrent, outputdict=True)
                summaryresults.append({
                    "Dataset": basename,
                    "Accuracy (Test)": round(bestreporttest["accuracy"], 4),
                    "Accuracy (Current)": round(reportcurrent["accuracy"], 4),
                    "Best Features": bestfeatures
                })
            else:
                summaryresults.append({
                    "Dataset": basename,
                    "Accuracy (Test)": round(bestreporttest["accuracy"], 4),
                    "Accuracy (Current)": None,
                    "Best Features": bestfeatures
                })
        else:
            summaryresults.append({
                "Dataset": basename,
                "Accuracy (Test)": round(bestreporttest["accuracy"], 4),
                "Accuracy (Current)": None,
                "Best Features": bestfeatures
            })

    # Final summary
    if summaryresults:
        print("\n FINAL SUMMARY")
        print("=" * 80)
        print(pd.DataFrame(summaryresults).tostring(index=False))
    else:
        print("No models evaluated or predictions made.")

def main():
    runpredictions()

if name == "main":
    main()
