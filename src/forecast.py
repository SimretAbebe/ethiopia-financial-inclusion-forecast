import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from typing import Dict

from src.impact_model import combine_events_for_indicator, INDICATOR_CALIBRATION


# 1. Trend fitting
def fit_linear_trend(df: pd.DataFrame, column: str):
    """Fit OLS linear trend: value ~ year. Returns model + forecast for 2025-2027."""
    df = df.copy()
    df["value_numeric"] = pd.to_numeric(df[column], errors="coerce")
    df = df.dropna(subset=["value_numeric"])
    df["year_num"] = df["year"] - df["year"].min()

    X = sm.add_constant(df[["year_num"]])
    y = df["value_numeric"]
    model = sm.OLS(y, X).fit()

    future_years = pd.DataFrame({"year": [2025, 2026, 2027]})
    future_years["year_num"] = future_years["year"] - df["year"].min()
    X_future = sm.add_constant(future_years[["year_num"]], has_constant="add")
    preds = model.get_prediction(X_future)
    forecast = preds.summary_frame(alpha=0.05)
    forecast["year"] = future_years["year"].values
    return model, forecast


def fit_log_trend(df: pd.DataFrame, column: str):
    df = df.copy()
    df["value_numeric"] = pd.to_numeric(df[column], errors="coerce")
    df = df.dropna(subset=["value_numeric"])          
    df["year_num"] = df["year"] - df["year"].min()

    X = sm.add_constant(df[["year_num"]])
    y = np.log(df["value_numeric"])
    model = sm.OLS(y, X).fit()

    future_years = pd.DataFrame({"year": [2025, 2026, 2027]})
    future_years["year_num"] = future_years["year"] - df["year"].min()
    X_future = sm.add_constant(future_years[["year_num"]], has_constant="add")
    preds = model.get_prediction(X_future)
    forecast = preds.summary_frame(alpha=0.05)
    forecast["mean"] = np.exp(forecast["mean"])
    forecast["obs_ci_lower"] = np.exp(forecast["obs_ci_lower"])
    forecast["obs_ci_upper"] = np.exp(forecast["obs_ci_upper"])
    forecast["year"] = future_years["year"].values
    return model, forecast



# 2. Event augmentation (reuses Task 3's impact_model directly)

def event_contribution_by_year(indicator_code, impact_df, events_df, years,
                                strength_multiplier=1.0, ramp_months=12):
    calibration_factor = INDICATOR_CALIBRATION.get(indicator_code, 1.0)
    contributions = []
    for yr in years:
        snapshot_date = pd.Timestamp(f"{yr}-12-31")
        raw_total, _ = combine_events_for_indicator(
            snapshot_date, indicator_code, impact_df, events_df, ramp_months=ramp_months
        )
        contributions.append(raw_total * calibration_factor * strength_multiplier)
    return pd.Series(contributions, index=years)


def add_event_effects(trend_forecast: pd.DataFrame, indicator_code, impact_df, events_df,
                       strength_multiplier=1.0) -> pd.DataFrame:
    """Adds 'event_contribution' and 'with_events' columns to a trend forecast."""
    forecast = trend_forecast.copy()
    event_contrib = event_contribution_by_year(
        indicator_code, impact_df, events_df, forecast["year"].tolist(),
        strength_multiplier=strength_multiplier
    )
    forecast["event_contribution"] = event_contrib.values
    forecast["with_events"] = forecast["mean"] + forecast["event_contribution"]
    return forecast


# 3. Scenario generation

SCENARIO_STRENGTH = {
    "base": 1.0,          
    "optimistic": 1.7,   
}


def generate_scenarios(trend_forecast: pd.DataFrame, indicator_code, impact_df, events_df,
                        scenario_strength: dict = None) -> Dict[str, pd.Series]:
    """Builds optimistic/base/pessimistic scenarios by varying event-effect strength."""
    scenario_strength = scenario_strength or SCENARIO_STRENGTH
    scenarios = {}
    for name, strength in scenario_strength.items():
        fc = add_event_effects(trend_forecast, indicator_code, impact_df, events_df,
                                strength_multiplier=strength)
        scenarios[name] = fc.set_index("year")["with_events"]
    return scenarios

# 4. Export helper
def export_forecast_table(trend_forecast: pd.DataFrame, scenarios: Dict[str, pd.Series],
                           metric_name: str, outfile: str) -> pd.DataFrame:
    """Builds and saves: year, metric, baseline trend, CI bounds, each scenario."""
    rows = []
    for _, row in trend_forecast.iterrows():
        yr = row["year"]
        entry = {
            "year": yr,
            "metric": metric_name,
            "baseline_trend": round(row["mean"], 2),
            "lower_ci": round(row["obs_ci_lower"], 2),
            "upper_ci": round(row["obs_ci_upper"], 2),
        }
        for scen_name, series in scenarios.items():
            entry[scen_name] = round(series.loc[yr], 2)
        rows.append(entry)

    table = pd.DataFrame(rows)
    table.to_csv(outfile, index=False)
    return table


# 5. Scenario visualization

def plot_forecast_with_scenarios(history_df, trend_forecast, scenarios, title, ylabel,
                                  value_column="value_numeric"):
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(history_df["year"], history_df[value_column],
            marker="o", linewidth=2, color="#1e293b", label="Historical")

    ax.plot(trend_forecast["year"], trend_forecast["mean"],
            marker="o", linestyle="--", color="#2563eb", label="Baseline trend")
    ax.fill_between(trend_forecast["year"], trend_forecast["obs_ci_lower"],
                     trend_forecast["obs_ci_upper"], color="#2563eb", alpha=0.15,
                     label="95% CI")

    colors = {"optimistic": "#16a34a", "base": "#2563eb", "pessimistic": "#dc2626"}
    for name, series in scenarios.items():
        ax.plot(series.index, series.values, marker="s", linestyle=":",
                color=colors.get(name, "#7c3aed"), label=f"{name.capitalize()} scenario")

    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.set_ylabel(ylabel)
    ax.set_xlabel("Year")
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    return fig