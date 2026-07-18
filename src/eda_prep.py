import pandas as pd


def get_indicator_series(df, indicator_code, record_type_column="record_type",
                          code_column="indicator_code", date_column="observation_date"):
    mask = (df[record_type_column] == "observation") & (df[code_column] == indicator_code)
    series = df[mask].copy()
    series[date_column] = pd.to_datetime(series[date_column], errors="coerce")
    series = series.sort_values(date_column)
    return series[[date_column, "value_numeric"]].reset_index(drop=True)


def resolve_duplicate_dates(series_df, date_column="observation_date",
                             value_column="value_numeric", method="mean"):
    return (series_df
            .groupby(date_column, as_index=False)[value_column]
            .agg(method))


def calculate_growth(series_df, value_column="value_numeric"):
    series_df = series_df.copy()
    series_df["pp_change"] = series_df[value_column].diff()
    series_df["years_between"] = series_df["observation_date"].diff().dt.days / 365.25
    series_df["annualized_rate"] = series_df["pp_change"] / series_df["years_between"]
    return series_df


def filter_by_pillar(df, pillar, record_type_column="record_type",
                      pillar_column="pillar"):
    mask = (df[record_type_column] == "observation") & (df[pillar_column] == pillar)
    return df[mask].copy()