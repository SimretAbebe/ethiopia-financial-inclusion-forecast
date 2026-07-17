def get_valid_codes(reference_df, field_name):
    matches = reference_df[reference_df["field"] == field_name]
    return set(matches["code"].tolist())


def find_invalid_values(df, reference_df, column, field_name=None):
    field_name = field_name or column
    valid_codes = get_valid_codes(reference_df, field_name)

    actual_values = set(df[column].dropna().unique())
    invalid = actual_values - valid_codes
    return invalid


def validate_all(df, reference_df):
    checks = {
        "record_type": "record_type",
        "pillar": "pillar",
        "confidence": "confidence",
        "category": "category",
    }

    for column, field_name in checks.items():
        if column not in df.columns:
            continue
        invalid = find_invalid_values(df, reference_df, column, field_name)
        if invalid:
            print(f"[FAIL] Column '{column}' has unexpected values: {invalid}")
        else:
            print(f"[OK]   Column '{column}' - all values match reference_codes")