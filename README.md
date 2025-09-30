# Algo Trading Models Using Python Part 1

This repository demonstrates my ability to build modular, end-to-end Python workflows for structured data:
- Data ingestion and validation
- Data cleaning (types, missing values, duplicates)
- Feature engineering (lags, rolling windows, groupby aggregates, time keys)
- Normalization with scikit-learn
- Predictive modeling with logistic regression
- Batch processing across multiple datasets
- Lightweight analysis (EDA, correlations, grouped summaries)
- Saving clean outputs and summary reports

Important: Core formulas, domain-specific features, and proprietary logic have been **intentionally abstracted** with placeholders (e.g., `Feature_A`, `Signal_X`, `Custom_Indicator`) to protect sensitive details. The code is a **skills showcase**, not a production-ready solution.

## Structure
- `config.py` — Central config for directories, file suffixes, and abstracted feature names.
- `ingest.py` — Example ingest and append workflow (with schema alignment).
- `clean.py` — Reusable cleaning utilities.
- `features.py` — Feature engineering showcase with placeholders.
- `normalize.py` — Train-fit normalization applied to current data.
- `src/pred.py` — Automated training, evaluation, and prediction pipeline.
- `requirements.txt` — Minimal dependencies.



