import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

from src import data_loader, eda_prep, impact_model as im, impact_matrix as imx, forecast as fc


st.set_page_config(
    page_title="Ethiopia Financial Inclusion Forecaster",
    page_icon="🇪🇹",
    layout="wide",
    initial_sidebar_state="expanded",
)

PRIMARY = "#4F46E5"     # indigo
ACCENT = "#F59E0B"      # amber
DANGER = "#F43F5E"      # rose
BLUE = "#0EA5E9"        # sky blue

st.markdown(f"""
<style>
    .main {{ background-color: #FAFAFA; }}
    .metric-card {{
        background: white; border-radius: 12px; padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06); border-left: 5px solid {PRIMARY};
    }}
    h1, h2, h3 {{ color: #1a1a2e; }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 8px; }}
    .stTabs [data-baseweb="tab"] {{
        background-color: #f0f2f6; border-radius: 8px 8px 0 0; padding: 8px 20px;
    }}
    .stTabs [aria-selected="true"] {{ background-color: {PRIMARY}; color: white; }}
    .badge {{
        display: inline-block; padding: 3px 10px; border-radius: 12px;
        font-size: 12px; font-weight: 600; color: white;
    }}
</style>
""", unsafe_allow_html=True)



@st.cache_data
def load_data():
    data = data_loader.load_all()
    main_df = data["main"]
    impact_df = data["impact"]
    events_df = main_df[main_df["record_type"] == "event"].copy()
    events_df["observation_date"] = pd.to_datetime(events_df["observation_date"])
    return main_df, impact_df, events_df


@st.cache_data
def get_yearly_series(_main_df, indicator_code):
    series = eda_prep.get_indicator_series(_main_df, indicator_code)
    series = eda_prep.resolve_duplicate_dates(series)
    series["year"] = pd.to_datetime(series["observation_date"]).dt.year
    return series


main_df, impact_df, events_df = load_data()

INDICATOR_LABELS = {
    "ACC_OWNERSHIP": "Account Ownership Rate (Access)",
    "ACC_MM_ACCOUNT": "Mobile Money Account Rate",
    "ACC_FAYDA": "Fayda Digital ID Enrollment",
    "ACC_4G_COV": "4G Population Coverage",
    "USG_P2P_COUNT": "P2P Transaction Count",
    "USG_CROSSOVER": "P2P/ATM Crossover Ratio",
    "USG_ACTIVE_RATE": "Mobile Money Activity Rate (Usage proxy)",
    "GEN_GAP_ACC": "Account Ownership Gender Gap",
}

TARGET_ACCESS = 60.0  # consortium's 60% Access target


def indicator_options(min_points=1):
    obs = main_df[main_df["record_type"] == "observation"]
    counts = obs["indicator_code"].value_counts()
    valid = [c for c in counts.index if counts[c] >= min_points and c in INDICATOR_LABELS]
    return valid


st.sidebar.markdown("## 🇪🇹 Ethiopia FI Forecaster")
st.sidebar.markdown("Selam Analytics — Financial Inclusion Forecasting")
page = st.sidebar.radio(
    "Navigate",
    ["Overview", "Trends", "Forecasts", "Inclusion Projections"],
    label_visibility="collapsed",
)
st.sidebar.markdown("---")
st.sidebar.caption(
    "Data sources: Global Findex, National Bank of Ethiopia, Shega News. "
    "Last updated per data_enrichment_log.md."
)


def page_overview():
    st.title("Overview")
    st.caption("Key financial inclusion metrics for Ethiopia at a glance.")

    acc = get_yearly_series(main_df, "ACC_OWNERSHIP")
    mm = get_yearly_series(main_df, "ACC_MM_ACCOUNT")
    acc_growth = eda_prep.calculate_growth(acc)

    latest_acc = acc["value_numeric"].iloc[-1]
    latest_mm = mm["value_numeric"].iloc[-1]
    latest_growth = acc_growth["annualized_rate"].iloc[-1]

    crossover_row = main_df[(main_df["indicator_code"] == "USG_CROSSOVER")]
    crossover_val = crossover_row["value_numeric"].iloc[-1] if not crossover_row.empty else None

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Account Ownership (Access)", f"{latest_acc:.1f}%",
                   f"{latest_growth:+.2f} pp/yr")
    with col2:
        st.metric("Mobile Money Account Rate", f"{latest_mm:.1f}%")
    with col3:
        if crossover_val is not None:
            label = "P2P > ATM" if crossover_val > 1 else "ATM > P2P"
            st.metric("P2P / ATM Crossover Ratio", f"{crossover_val:.2f}x", label)
        else:
            st.metric("P2P / ATM Crossover Ratio", "N/A")
    with col4:
        gap_to_target = TARGET_ACCESS - latest_acc
        st.metric("Gap to 60% Access Target", f"{gap_to_target:.1f} pp")

    st.markdown("---")

    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("Growth Rate by Survey Period")
        gdf = acc_growth.dropna(subset=["annualized_rate"]).copy()
        gdf["period"] = gdf["observation_date"].dt.year.astype(str)
        fig = px.bar(gdf, x="period", y="annualized_rate", color="annualized_rate",
                     color_continuous_scale=["#F43F5E", "#F59E0B", "#4F46E5"],
                     labels={"annualized_rate": "pp / year", "period": "Survey year"})
        fig.update_layout(showlegend=False, coloraxis_showscale=False, height=350)
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Growth decelerated sharply after 2021 despite major mobile money launches.")

    with c2:
        st.subheader("Data Coverage")
        obs = main_df[main_df["record_type"] == "observation"]
        st.write(f"**{len(obs)}** total observations")
        st.write(f"**{len(events_df)}** cataloged events")
        st.write(f"**{len(impact_df)}** modeled impact links")
        counts = obs["source_type"].value_counts()
        fig2 = px.pie(values=counts.values, names=counts.index, hole=0.5,
                      color_discrete_sequence=px.colors.sequential.Purples_r)
        fig2.update_layout(height=250, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig2, use_container_width=True)



def page_trends():
    st.title("Trends Explorer")
    st.caption("Interactive time series across all tracked indicators.")

    options = indicator_options(min_points=1)
    labels = [INDICATOR_LABELS.get(o, o) for o in options]

    selected_labels = st.multiselect(
        "Select indicators to compare", labels, default=labels[:2]
    )
    selected_codes = [o for o, l in zip(options, labels) if l in selected_labels]

    normalize = st.checkbox(
        "Normalize to % change from first observation (recommended when comparing "
        "indicators with very different scales/units)", value=len(selected_codes) > 1
    )

    if not selected_codes:
        st.info("Select at least one indicator above.")
        return

    fig = go.Figure()
    all_years = []
    for code in selected_codes:
        series = get_yearly_series(main_df, code)
        all_years.extend(series["year"].tolist())
        y = series["value_numeric"]
        if normalize and y.iloc[0] != 0:
            y = (y / y.iloc[0] - 1) * 100
        fig.add_trace(go.Scatter(
            x=series["observation_date"], y=y, mode="lines+markers",
            name=INDICATOR_LABELS.get(code, code)
        ))

    if all_years:
        yr_min, yr_max = min(all_years), max(all_years)
        date_range = st.slider("Date range (year)", int(yr_min), int(yr_max),
                                (int(yr_min), int(yr_max)))
        fig.update_xaxes(range=[f"{date_range[0]}-01-01", f"{date_range[1]}-12-31"])

    fig.update_layout(
        height=500,
        yaxis_title="% change from first value" if normalize else "Value",
        xaxis_title="Date",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    fig.update_xaxes(rangeslider_visible=True)
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("Download underlying data"):
        combined = pd.concat([
            get_yearly_series(main_df, c).assign(indicator=INDICATOR_LABELS.get(c, c))
            for c in selected_codes
        ])
        st.dataframe(combined)
        st.download_button("Download as CSV", combined.to_csv(index=False),
                            file_name="trends_data.csv", mime="text/csv")


#forecast
def page_forecasts():
    st.title("Forecasts 2025-2027")
    st.caption("Trend-based and event-augmented projections with confidence intervals.")

    target_choice = st.selectbox(
        "Select forecast target",
        ["Access: Account Ownership Rate", "Usage: Mobile Money Account Rate (proxy)"],
    )
    indicator_code = "ACC_OWNERSHIP" if "Access" in target_choice else "ACC_MM_ACCOUNT"

    model_choice = st.radio("Trend model", ["Linear", "Log-linear"], horizontal=True)

    series = get_yearly_series(main_df, indicator_code)
    if len(series) < 2:
        st.warning(f"Not enough data points to fit a trend for {indicator_code}.")
        return

    fit_fn = fc.fit_linear_trend if model_choice == "Linear" else fc.fit_log_trend
    try:
        model, trend_forecast = fit_fn(series, "value_numeric")
    except Exception as e:
        st.error(f"Could not fit {model_choice} trend: {e}")
        return

    scenarios = fc.generate_scenarios(trend_forecast, indicator_code, impact_df, events_df)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=series["year"], y=series["value_numeric"],
                              mode="lines+markers", name="Historical",
                              line=dict(color="#1a1a2e", width=3)))
    fig.add_trace(go.Scatter(x=trend_forecast["year"], y=trend_forecast["mean"],
                              mode="lines+markers", name="Baseline trend",
                              line=dict(color=BLUE, dash="dash")))
    fig.add_trace(go.Scatter(
        x=list(trend_forecast["year"]) + list(trend_forecast["year"][::-1]),
        y=list(trend_forecast["obs_ci_upper"]) + list(trend_forecast["obs_ci_lower"][::-1]),
        fill="toself", fillcolor="rgba(37,99,235,0.15)", line=dict(color="rgba(0,0,0,0)"),
        name="95% Confidence Interval",
    ))
    colors = {"optimistic": PRIMARY, "base": BLUE, "pessimistic": DANGER}
    for name, s in scenarios.items():
        fig.add_trace(go.Scatter(x=s.index, y=s.values, mode="lines+markers",
                                  name=f"{name.capitalize()} scenario",
                                  line=dict(color=colors.get(name), dash="dot")))

    fig.update_layout(height=500, xaxis_title="Year", yaxis_title="% of adults",
                       hovermode="x unified",
                       legend=dict(orientation="h", yanchor="bottom", y=1.02))
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Key Projected Milestones")
    cols = st.columns(len(scenarios)) if scenarios else [st.container()]
    for col, (name, s) in zip(cols, scenarios.items()):
        with col:
            value = f"{s.loc[2027]:.1f}%" if 2027 in s.index else "N/A"
            st.metric(f"2027 {name.capitalize()}", value)

    table = fc.export_forecast_table(trend_forecast, scenarios, target_choice,
                                      "/tmp/_dashboard_forecast.csv")
    with st.expander("View / download forecast table"):
        st.dataframe(table)
        st.download_button("Download forecast as CSV", table.to_csv(index=False),
                            file_name=f"{indicator_code}_forecast.csv", mime="text/csv")

    if indicator_code == "ACC_MM_ACCOUNT":
        st.info("This series has only 2 historical data points - treat this forecast "
                "as illustrative, not statistically robust.")


#inclusion projections
def page_projections():
    st.title("Inclusion Projections")
    st.caption("Progress toward the consortium's financial inclusion targets.")

    scenario = st.select_slider(
        "Select scenario", options=["Pessimistic", "Base", "Optimistic"], value="Base"
    )
    scenario_key = scenario.lower()

    acc_series = get_yearly_series(main_df, "ACC_OWNERSHIP")
    model, trend_forecast = fc.fit_linear_trend(acc_series, "value_numeric")
    scenarios = fc.generate_scenarios(trend_forecast, "ACC_OWNERSHIP", impact_df, events_df)
    projected_2027 = scenarios[scenario_key].loc[2027]

    col1, col2 = st.columns([1, 1])
    with col1:
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=projected_2027,
            delta={"reference": TARGET_ACCESS, "increasing": {"color": DANGER},
                   "decreasing": {"color": PRIMARY}},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": PRIMARY},
                "steps": [
                    {"range": [0, 40], "color": "#fde2e1"},
                    {"range": [40, 60], "color": "#fff3cd"},
                    {"range": [60, 100], "color": "#d4edda"},
                ],
                "threshold": {"line": {"color": DANGER, "width": 4},
                              "thickness": 0.9, "value": TARGET_ACCESS},
            },
            title={"text": f"2027 Access Projection ({scenario} scenario)"},
        ))
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Scenario Comparison, 2025-2027")
        fig2 = go.Figure()
        colors = {"optimistic": PRIMARY, "base": BLUE, "pessimistic": DANGER}
        for name, s in scenarios.items():
            fig2.add_trace(go.Scatter(x=s.index, y=s.values, mode="lines+markers",
                                       name=name.capitalize(),
                                       line=dict(color=colors.get(name))))
        fig2.add_hline(y=TARGET_ACCESS, line_dash="dash", line_color=DANGER,
                        annotation_text="60% Target")
        fig2.update_layout(height=350, xaxis_title="Year", yaxis_title="% of adults")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.subheader("Answers to the Consortium's Key Questions")

    with st.expander("What drives financial inclusion in Ethiopia?", expanded=True):
        st.write(
            "Product launches (Telebirr, M-Pesa), digital ID rollout (Fayda), and "
            "regulatory interoperability directives are the main modeled drivers. "
            "However, most links remain qualitative estimates - only the Telebirr/M-Pesa "
            "effect on Mobile Money Account Rate has been calibrated against real data."
        )
    with st.expander("Why did account ownership stagnate despite 65M+ mobile money accounts?"):
        st.write(
            "Likely a saturation/denominator effect: most new mobile money sign-ups may "
            "be reaching adults who already had a bank account, rather than the previously "
            "unbanked (mobile-money-only users are rare in Ethiopia, ~0.5%)."
        )
    with st.expander("What data gaps most limit this analysis?"):
        st.write(
            "Extremely sparse time series (most indicators have 1-2 points ever), no "
            "dedicated 'digital payment usage %' indicator matching the Findex definition, "
            "and only one calibrated impact estimate out of many hypothesized links."
        )

    if projected_2027 < TARGET_ACCESS:
        st.warning(f"Under the **{scenario}** scenario, projected 2027 Access "
                   f"({projected_2027:.1f}%) falls short of the 60% target by "
                   f"{TARGET_ACCESS - projected_2027:.1f} percentage points.")
    else:
        st.success(f"Under the **{scenario}** scenario, projected 2027 Access "
                   f"({projected_2027:.1f}%) meets or exceeds the 60% target.")


#routers
if page == "Overview":
    page_overview()
elif page == "Trends":
    page_trends()
elif page == "Forecasts":
    page_forecasts()
elif page == "Inclusion Projections":
    page_projections()