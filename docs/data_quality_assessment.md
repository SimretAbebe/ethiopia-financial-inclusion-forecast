# Data Quality Assessment

## 1. Extremely sparse time series
Most indicators have only 1-2 observations EVER recorded. Only
ACC_OWNERSHIP (6 points) and ACC_FAYDA (4 points) have enough data to
show any real trend. This severely limits statistical analysis (e.g.
correlation, regression) - most techniques assume many data points, not 2-6.

## 2. Conflicting values for the same indicator and date
Three different Account Ownership values are all dated 2021-12-31 (46%,
56%, 36%) - a 20 percentage-point spread for the same supposed measurement.
This was resolved for charting purposes by averaging (see
`eda_prep.resolve_duplicate_dates()`), but the underlying disagreement is
not explained by the dataset itself - likely different sources or
sub-populations were merged without being labeled distinctly.

## 3. Uneven pillar coverage
ACCESS and USAGE dominate the observations (as expected, since they're the
forecasting targets). QUALITY, TRUST, and DEPTH have zero observations,
despite being valid pillars in reference_codes.xlsx. Any claims about these
pillars would be pure speculation with the current data.

## 4. Correlation results are statistically unreliable
Because most indicator pairs share only 2 overlapping yearly values,
computed correlations (e.g. +1.0, -1.0) are mathematical artifacts of small
sample size, not evidence of real relationships. These should NOT be used
as-is for forecasting or policy claims without much more data.

## 5. Events are not yet causally validated, only hypothesized
The impact_link records (including the ones added during Task 1 enrichment)
represent REASONED HYPOTHESES about event effects - some backed by direct
Ethiopian data ("empirical"), others by comparable-country research
("literature"), and some by pure logical reasoning ("theoretical"). None of
these have been statistically tested yet - that is deferred to the impact
modeling phase (Task 3).

## 6. Survey years are unevenly spaced
Global Findex surveys occurred in 2011, 2014, 2017, 2021, 2024 - gaps of
3, 3, 4, and 3 years respectively. This means "growth between surveys" is
not directly comparable without annualizing (dividing by the number of
years), which was done in `eda_prep.calculate_growth()` - raw point-to-point
differences would otherwise overstate change in the 4-year 2017-2021 gap
relative to the 3-year gaps.

## 7. New 2025-2026 observations added during enrichment differ in nature
from the original Findex-based observations
The original ACC_OWNERSHIP/ACC_MM_ACCOUNT figures come from Global Findex
household surveys (nationally representative). Some enrichment additions
(e.g. total accounts/wallets from Shega News) come from operator/registry
counts, which may include duplicate accounts per person or inactive
accounts - these are NOT directly equivalent to Findex's "adults with an
account" definition and should be treated as context/corroboration, not a
like-for-like replacement.