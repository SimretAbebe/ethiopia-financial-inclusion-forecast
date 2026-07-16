# Ethiopia Financial Inclusion Forecasting

A forecasting system that tracks Ethiopia's digital financial transformation,
predicting **Access** (account ownership) and **Usage** (digital payment adoption)
for 2025-2027, based on the World Bank's Global Findex framework.

## Project Structure

```text
.github/
└── workflows/
    └── unittests.yml

data/
├── raw/
│   ├── ethiopia_fi_unified_data.csv
│   └── reference_codes.csv
└── processed/

notebooks/
└── README.md

src/
└── __init__.py

dashboard/
└── app.py

tests/
└── __init__.py

models/
reports/
└── figures/

requirements.txt
README.md
.gitignore
```

## Setup

```bash
pip install -r requirements.txt
```
