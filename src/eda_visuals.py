import matplotlib.pyplot as plt
import pandas as pd


def plot_indicator_trend(series_df, title, ylabel,
                          date_column="observation_date", value_column="value_numeric"):
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(series_df[date_column], series_df[value_column],
            marker="o", linewidth=2, color="#2563eb")
    for _, row in series_df.iterrows():
        ax.annotate(f"{row[value_column]:.0f}",
                    (row[date_column], row[value_column]),
                    textcoords="offset points", xytext=(0, 10), fontsize=9)
    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.set_ylabel(ylabel)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    return fig


def plot_growth_rates(growth_df, title, date_column="observation_date"):
    fig, ax = plt.subplots(figsize=(9, 5))
    labels = growth_df[date_column].dt.year.astype("Int64").astype(str)
    ax.bar(labels, growth_df["annualized_rate"], color="#16a34a")
    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.set_ylabel("Annualized change (pp/year)")
    ax.axhline(0, color="black", linewidth=0.8)
    fig.tight_layout()
    return fig


def plot_event_timeline(events_df, date_column="observation_date",
                         name_column="indicator", category_column="category"):
    events_df = events_df.sort_values(date_column).reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.scatter(events_df[date_column], [1] * len(events_df),
               s=80, color="#dc2626", zorder=3)
    for i, row in events_df.iterrows():
        y_offset = 1.05 if i % 2 == 0 else 0.95
        ax.annotate(f"{row[name_column]}\n({row[category_column]})",
                    (row[date_column], 1),
                    xytext=(row[date_column], y_offset),
                    ha="center", fontsize=8, rotation=0,
                    arrowprops=dict(arrowstyle="-", alpha=0.4))
    ax.set_yticks([])
    ax.set_title("Event Timeline", fontsize=13, fontweight="bold")
    fig.tight_layout()
    return fig


def plot_trend_with_events(series_df, events_df, title, ylabel,
                            date_column="observation_date", value_column="value_numeric",
                            event_date_column="observation_date", event_name_column="indicator"):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(series_df[date_column], series_df[value_column],
            marker="o", linewidth=2, color="#2563eb", zorder=3)

    for _, row in events_df.iterrows():
        ax.axvline(row[event_date_column], color="#dc2626", linestyle="--", alpha=0.5)

    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.set_ylabel(ylabel)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    return fig


def plot_coverage_heatmap(df, record_type_column="record_type",
                           indicator_column="indicator", date_column="observation_date"):
    obs = df[df[record_type_column] == "observation"].copy()
    obs[date_column] = pd.to_datetime(obs[date_column], errors="coerce")
    obs["year"] = obs[date_column].dt.year

    pivot = pd.crosstab(obs[indicator_column], obs["year"])
    pivot = (pivot > 0).astype(int)

    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(pivot.values, cmap="Blues", aspect="auto")
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(pivot.columns, rotation=45)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index, fontsize=8)
    ax.set_title("Indicator Coverage by Year", fontsize=13, fontweight="bold")
    fig.tight_layout()
    return fig