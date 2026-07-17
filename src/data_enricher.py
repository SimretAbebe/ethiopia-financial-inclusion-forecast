import pandas as pd
from datetime import date


def new_observation(pillar, indicator, indicator_code, value_numeric,
                     observation_date, source_name, source_url, confidence,
                     unit=None, original_text=None, collected_by=None,
                     collection_date=None, notes=None, gender="all",
                     location="national", period_start=None, period_end=None):
    return {
        "record_type": "observation",
        "pillar": pillar,
        "indicator": indicator,
        "indicator_code": indicator_code,
        "value_numeric": value_numeric,
        "unit": unit,
        "observation_date": observation_date,
        "period_start": period_start,
        "period_end": period_end,
        "gender": gender,
        "location": location,
        "source_name": source_name,
        "source_url": source_url,
        "confidence": confidence,
        "original_text": original_text,
        "collected_by": collected_by,
        "collection_date": collection_date or date.today().isoformat(),
        "notes": notes,
    }


def new_event(record_id, category, indicator, observation_date,
              source_name, source_url, confidence,
              original_text=None, collected_by=None,
              collection_date=None, notes=None):
    return {
        "record_id": record_id,
        "record_type": "event",
        "category": category,
        "pillar": None,
        "indicator": indicator,
        "observation_date": observation_date,
        "source_name": source_name,
        "source_url": source_url,
        "confidence": confidence,
        "original_text": original_text,
        "collected_by": collected_by,
        "collection_date": collection_date or date.today().isoformat(),
        "notes": notes,
    }


def new_impact_link(parent_id, pillar, related_indicator, impact_direction,
                     impact_magnitude, lag_months, evidence_basis,
                     relationship_type="direct", confidence="medium",
                     collected_by=None, collection_date=None, notes=None):
    return {
        "parent_id": parent_id,
        "record_type": "impact_link",
        "pillar": pillar,
        "related_indicator": related_indicator,
        "relationship_type": relationship_type,
        "impact_direction": impact_direction,
        "impact_magnitude": impact_magnitude,
        "lag_months": lag_months,
        "evidence_basis": evidence_basis,
        "confidence": confidence,
        "collected_by": collected_by,
        "collection_date": collection_date or date.today().isoformat(),
        "notes": notes,
    }


def append_records(original_df, new_records):
    new_df = pd.DataFrame(new_records)
    combined = pd.concat([original_df, new_df], ignore_index=True, sort=False)
    return combined