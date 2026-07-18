import pandas as pd

#reshape the data into wide format
def build_wide_indicator_table(df, record_type_column="record_type",
                                code_column="indicator_code",
                                date_column="observation_date",
                                value_column="value_numeric"):
    obs = df[df[record_type_column] == "observation"].copy()
    obs[date_column] = pd.to_datetime(obs[date_column], errors="coerce")
    obs["year"] = obs[date_column].dt.year

    wide = obs.pivot_table(index="year", columns=code_column,
                            values=value_column, aggfunc="mean")
    return wide


#compute pairwise correlation between every pair of indicator columns
def compute_correlation_matrix(wide_df, method="pearson"):
    return wide_df.corr(method=method, min_periods=2)


#full correlation matrix
def top_correlations_with(corr_matrix, target_indicator, top_n=5):
    if target_indicator not in corr_matrix.columns:
        raise ValueError(f"'{target_indicator}' not found in correlation matrix.")

    series = corr_matrix[target_indicator].drop(index=target_indicator)
    series = series.dropna()
    ranked = series.reindex(series.abs().sort_values(ascending=False).index)
    return ranked.head(top_n)