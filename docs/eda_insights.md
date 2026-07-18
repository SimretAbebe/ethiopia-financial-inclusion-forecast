# Task 2: EDA Key Insights

## 1. Account ownership growth decelerated sharply after 2021
Growth dropped from ~2.75 percentage points/year (2017-2021) to ~1.03 pp/year
(2021-2024) - a more than 60% slowdown in pace. This is despite Telebirr
(2021) and M-Pesa (2023) both launching in this exact window.
**Evidence:** `eda_prep.calculate_growth()` output on ACC_OWNERSHIP series.

## 2. The account-ownership slowdown likely reflects a saturation/denominator
## effect, not a lack of digital growth
Mobile money accounts and transaction volumes grew massively in the same
period (e.g. 9.7 trillion ETB in digital transactions in FY2023/24), yet
Findex account ownership barely moved. This suggests most new mobile money
sign-ups may be going to people who ALREADY had a bank account (per Sheet D:
"mobile money-only users are rare, ~0.5%"), rather than reaching previously
unbanked adults.
**Evidence:** Comparison of ACC_OWNERSHIP trend vs USG_DIGITAL_TXN_VALUE and
market-nuance context from the Additional Data Points Guide (Sheet D).

## 3. Data coverage is highly uneven across pillars and years
The coverage heatmap shows dense data clusters around 2024-2025 and almost
nothing for QUALITY, TRUST, or DEPTH pillars at any point in time. Several
indicators (e.g. M-Pesa Registered Users, ATM Transaction Value) have exactly
ONE data point ever recorded.
**Evidence:** `eda_visuals.plot_coverage_heatmap()` output.

## 4. Visual overlay does not show an obvious acceleration in account
## ownership immediately after Telebirr's launch
Plotting the account ownership trend with event dates overlaid does not show
a visible kink or acceleration in the trend line right after the Telebirr
launch (May 2021) marker. This is a useful negative finding - it suggests
Telebirr's effect on Access (if any) may be delayed, indirect, or too small
to see against a 3-year survey gap, rather than immediate and dramatic.
**Evidence:** `eda_visuals.plot_trend_with_events()` chart, Section 5.

## 5. Correlations computed from the dataset are mostly unreliable due to
## extremely small sample sizes
Several indicator pairs show correlation of exactly +1.0 or -1.0 (e.g.
ACC_OWNERSHIP vs ACC_MM_ACCOUNT). This is a mathematical artifact of having
only 2 overlapping yearly data points, not evidence of a real relationship.
Any 2 points are "perfectly" correlated by definition.
**Evidence:** `eda_correlation.top_correlations_with()` output.

## 6. The Fayda Digital ID rollout shows the clearest empirically-supported
## growth pattern in the entire dataset
Fayda enrollment grew from a 2024 baseline to 16.4M (Jun 2025) to 25M
(Sept 2025) - a clear, steep, well-documented acceleration, unlike most
other indicators which have too few points to show any trend at all.
**Evidence:** ACC_FAYDA observation series, cross-referenced with the Task 1
enrichment log sources (nbe.gov.et, shega.co).