import pandas as pd
from src import config


def load_main_sheet(filepath=None, sheet_name=None):
    path = filepath or config.UNIFIED_DATA_FILE
    sheet = sheet_name or config.SHEET_MAIN
    df = pd.read_excel(path, sheet_name=sheet)
    print(f"Loaded '{sheet}': {len(df)} rows, {len(df.columns)} columns")
    return df


def load_impact_sheet(filepath=None, sheet_name=None):
    path = filepath or config.UNIFIED_DATA_FILE
    sheet = sheet_name or config.SHEET_IMPACT
    df = pd.read_excel(path, sheet_name=sheet)
    print(f"Loaded '{sheet}': {len(df)} rows, {len(df.columns)} columns")
    return df


def load_reference_codes(filepath=None):
    path = filepath or config.REFERENCE_CODES_FILE
    df = pd.read_excel(path)
    print(f"Loaded reference codes: {len(df)} rows, {len(df.columns)} columns")
    return df


def load_all():
    return {
        "main": load_main_sheet(),
        "impact": load_impact_sheet(),
        "reference": load_reference_codes(),
    }