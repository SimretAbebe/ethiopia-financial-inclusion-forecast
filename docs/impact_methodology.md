# Task 3: Event Impact Modeling - Methodology

## 1. Modeling Approach
Each event's effect on an indicator is modeled as a **ramp function**, not an
instant jump:
- Before `lag_months` have passed since the event: effect = 0
- After the lag: effect increases linearly over `ramp_months` (default 12)
  until reaching full strength, then holds steady
- Multiple events affecting the same indicator are combined by **summing**
  their individual effects at any given date

## 2. Functional Form (Chosen and Why)
A linear ramp was chosen over an instant step-function because financial
behavior change (opening an account, adopting a habit) plausibly takes time
to spread through a population - it is not reasonable to assume every
affected person acts within the same month. A ramp is also simpler to
reason about and justify than an S-curve, given how little Ethiopian data
exists to fit a more complex shape.

## 3. Magnitude Encoding
Impact_link records describe magnitude qualitatively (high/medium/low).
These were encoded as relative weights: high=3.0, medium=1.5, low=0.5
(high is twice medium, medium is three times low) - a reasonable but
subjective starting scale, refined below through calibration.

## 4. Calibration Against Real Data (Step 5)
**Validated case: Telebirr (2021) + M-Pesa (2023) -> Mobile Money Account
Rate (ACC_MM_ACCOUNT).**
- Real observed change: 4.7% (2021) -> 9.45% (2024), i.e. +4.75 percentage points
- Raw model output (uncalibrated) at the same date: 1.125 units
- Calibration factor derived: 4.75 / 1.125 = 4.22
- This factor was applied ONLY to `ACC_MM_ACCOUNT`, not globally, since
  different indicators have different units and scales - a factor derived
  from one indicator cannot be assumed to generalize to others.

**Why the initial raw estimate undershot reality:** the "medium" magnitude
originally assigned to the M-Pesa-launch effect likely understated the
real-world combined effect of TWO overlapping product launches (Telebirr
and M-Pesa) plus broader digital payment ecosystem growth not captured by
any single impact_link. This suggests the model's linear summation may
still understate compounding/network effects between simultaneous events.

## 5. Comparable Country Evidence (Step 3)
For indicators without sufficient Ethiopian pre/post data, Kenya's M-Pesa
rollout provides the most relevant comparable case:
- M-Pesa Kenya reached ~70% adult adoption by 2011, ~4 years after its
  2007 launch (Jack & Suri, 2011/2014) - used to sanity-check that a
  "high magnitude, 12-24 month lag" assignment for major product launches
  is directionally reasonable, not overstated.
- Suri & Jack (2016) found mobile money access reduced poverty by 2
  percentage points in Kenya - used as qualitative support for assigning
  "medium" (not "high") magnitude to indirect/enabling effects, reserving
  "high" for direct, well-documented mechanisms.
This evidence is used for directional/qualitative calibration only, since
Kenya's market structure and starting conditions differ from Ethiopia's.

## 6. Confidence Levels (Step 6)
| Indicator | Calibrated? | Confidence |
|---|---|---|
| ACC_MM_ACCOUNT | Yes (factor 4.22) | High - validated against real Findex data |
| All other indicators (ACC_OWNERSHIP, USG_P2P_COUNT, ACC_FAYDA, etc.) | No (factor 1.0) | Low - raw qualitative estimates, not yet validated |

## 7. Key Assumptions
- Effects are linear ramps, not S-curves or instant jumps (a simplification)
- Multiple event effects simply add together (no interaction/compounding
  terms modeled, though Section 4 suggests real effects may compound)
- Magnitude words (high/medium/low) map to a fixed 3.0/1.5/0.5 relative
  scale before calibration
- Only one indicator (ACC_MM_ACCOUNT) has been validated against real data;
  all others remain qualitative, uncalibrated estimates

## 8. Limitations
- Calibration is based on a single validated data point (2021-2024 change);
  a single before/after comparison cannot separate Telebirr's effect from
  M-Pesa's effect, from broader ecosystem growth, or from measurement error
  in the underlying Findex survey itself
- No statistical significance testing was performed (insufficient data
  points for standard regression inference)
- Comparable-country evidence (Kenya) is used qualitatively only - Ethiopia's
  regulatory environment, agent network density, and starting financial
  infrastructure differ meaningfully from Kenya's 2007-2011 conditions
- The linear-ramp assumption is untested against alternative functional
  forms (e.g. S-curve, exponential decay) due to data limitations