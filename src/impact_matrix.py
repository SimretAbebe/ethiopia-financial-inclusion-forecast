import pandas as pd
from src.impact_model import MAGNITUDE_TO_NUMBER, INDICATOR_CALIBRATION

#builds the events x indicator matrix
def build_association_matrix(impact_df, calibration=None):
    calibration = calibration or INDICATOR_CALIBRATION
    df = impact_df.copy()

    df["magnitude_number"] = df["impact_magnitude"].map(MAGNITUDE_TO_NUMBER).fillna(0.0)
    df["sign"] = df["impact_direction"].apply(lambda d: 1 if d == "increase" else -1)
    df["raw_effect"] = df["sign"] * df["magnitude_number"]

    df["calibration_factor"] = df["related_indicator"].map(calibration).fillna(1.0)
    df["calibrated_effect"] = df["raw_effect"] * df["calibration_factor"]

    matrix = df.pivot_table(index="parent_id", columns="related_indicator",
                             values="calibrated_effect", aggfunc="sum")
    return matrix



#returns a small table for each indicator showing if it is calibrated
def build_confidence_flags(impact_df, calibration=None):
    calibration = calibration or INDICATOR_CALIBRATION
    indicators = impact_df["related_indicator"].unique()
    rows = []
    for ind in indicators:
        is_calibrated = ind in calibration
        rows.append({
            "indicator": ind,
            "calibrated": is_calibrated,
            "calibration_factor": calibration.get(ind, 1.0),
        })
    return pd.DataFrame(rows)