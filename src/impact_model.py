import pandas as pd
import numpy as np


MAGNITUDE_TO_NUMBER = {
    "high": 3.0,
    "medium": 1.5,
    "low": 0.5,
}


def event_effect_at(observation_date, event_date, lag_months, magnitude,
                     direction, ramp_months=12):
    months_since_event = (observation_date.year - event_date.year) * 12 \
                        + (observation_date.month - event_date.month)

    if months_since_event < lag_months:
        return 0.0

    months_into_ramp = months_since_event - lag_months
    progress = min(months_into_ramp / ramp_months, 1.0)

    full_strength = MAGNITUDE_TO_NUMBER.get(magnitude, 0.0)
    sign = 1 if direction == "increase" else -1

    return sign * full_strength * progress



# adds up the event into one event effect
def combine_events_for_indicator(observation_date, indicator_code, impact_df, events_df,
                                  event_id_column="parent_id",
                                  event_record_id_column="record_id",
                                  event_date_column="observation_date",
                                  ramp_months=12):
    relevant_links = impact_df[impact_df["related_indicator"] == indicator_code]

    total_effect = 0.0
    breakdown = []

    for _, link in relevant_links.iterrows():
        event_row = events_df[events_df[event_record_id_column] == link[event_id_column]]
        if event_row.empty:
            continue

        event_date = pd.to_datetime(event_row.iloc[0][event_date_column])

        effect = event_effect_at(
            observation_date=observation_date,
            event_date=event_date,
            lag_months=link["lag_months"],
            magnitude=link["impact_magnitude"],
            direction=link["impact_direction"],
            ramp_months=ramp_months,
        )

        total_effect += effect
        breakdown.append({"event_id": link[event_id_column], "effect": effect})

    return total_effect, breakdown


INDICATOR_CALIBRATION = {
    "ACC_MM_ACCOUNT": 4.22,  
}


def predict_indicator_change(observation_date, indicator_code, impact_df, events_df,
                              ramp_months=12):
    raw_total, breakdown = combine_events_for_indicator(
        observation_date, indicator_code, impact_df, events_df, ramp_months=ramp_months
    )
    calibration_factor = INDICATOR_CALIBRATION.get(indicator_code, 1.0)
    calibrated_total = raw_total * calibration_factor

    return calibrated_total, calibration_factor, breakdown