import pandas as pd


def count_by_column(df, column):
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in this DataFrame.")
    return df[column].value_counts(dropna=False)


def get_temporal_range(df, date_column="observation_date"):
    dates = pd.to_datetime(df[date_column], errors="coerce")
    return dates.min(), dates.max()


def indicator_coverage(df, indicator_column="indicator", record_type_column="record_type"):
    obs = df[df[record_type_column] == "observation"]
    return obs[indicator_column].value_counts()


def list_events(df, record_type_column="record_type",
                 name_column="indicator", date_column="observation_date",
                 category_column="category"):
    events = df[df[record_type_column] == "event"].copy()
    events = events.sort_values(date_column)
    return events[[name_column, category_column, date_column]]


def duplicate_check(df, indicator_column="indicator_code",
                     date_column="observation_date",
                     record_type_column="record_type"):
    obs = df[df[record_type_column] == "observation"]
    grouped = obs.groupby([indicator_column, date_column]).size()
    return grouped[grouped > 1]


def summarize(df):
    print("=== Record Type Counts ===")
    print(count_by_column(df, "record_type"))
    print("\n=== Pillar Counts (NaN = events) ===")
    print(count_by_column(df, "pillar"))
    print("\n=== Confidence Counts ===")
    print(count_by_column(df, "confidence"))
    print("\n=== Temporal Range ===")
    min_date, max_date = get_temporal_range(df)
    print(f"Earliest: {min_date} | Latest: {max_date}")
    print("\n=== Indicator Coverage ===")
    print(indicator_coverage(df))
    print("\n=== Events, in order ===")
    print(list_events(df).to_string(index=False))
    print("\n=== Duplicate date/indicator flags ===")
    dupes = duplicate_check(df)
    print(dupes if len(dupes) > 0 else "None found.")