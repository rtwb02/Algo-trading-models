"""
Centralized configuration for the showcase repository.

All paths, suffixes, and feature names are abstracted to protect proprietary details.
"""

import os

Base directory for all data; customize or set via environment variable
BASEDIR = os.environ.get("SHOWCASEBASEDIR", "path/to/data")

Data subdirectories
SPLITDIR = os.path.join(BASEDIR, "splits")          # expected: Train.csv, Test.csv
CURRENTDIR = os.path.join(BASEDIR, "current")        # expected: Current.csv or CurrentProcessed.csv
NORMALIZEDDIR = os.path.join(BASEDIR, "normalized")  # outputs: CurrentNorm.csv / TestNorm.csv
PREDICTIONSDIR = os.path.join(BASEDIR, "predictions")
REPORTSDIR = os.path.join(BASEDIR, "reports")

Ensure output directories exist
for d in [NORMALIZEDDIR, PREDICTIONSDIR, REPORTSDIR]:
    os.makedirs(d, existok=True)

File suffixes (abstracted)
TRAINSUFFIX = "Train.csv"
TESTSUFFIX = "Test.csv"
CURRENTSUFFIX = "Current.csv"
CURRENTPROCESSEDSUFFIX = "CurrentProcessed.csv"
TESTCLEANEDSUFFIX = "TestCleaned.csv"
TRAINCLEANEDSUFFIX = "TrainCleaned.csv"
TESTNORMSUFFIX = "TestNorm.csv"
CURRENTNORMSUFFIX = "CurrentNorm.csv"

Target column (abstracted)
TARGETCOL = "Target"

Candidate features (abstracted naming patterns)
CANDIDATEFEATUREPREFIXES = ["Feature", "Signal", "Metric"]
LAGSUFFIX = "Lag1"

Example set of columns to normalize (abstracted)
NORMALIZECOLS = [
    "FeatureA", f"FeatureA{LAGSUFFIX}",
    "FeatureB", f"FeatureB{LAGSUFFIX}",
    "FeatureC", f"FeatureC{LAGSUFFIX}",
    "SignalX", f"SignalX{LAGSUFFIX}",
]

Columns excluded from modeling
EXCLUDEFEATURES = ["Date", "Open", "High", "Low", "Close", "Volume", TARGET_COL]
