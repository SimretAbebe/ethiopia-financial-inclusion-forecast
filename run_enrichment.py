import pandas as pd
import os
from src import data_loader
from src import data_enricher as enrich
import build_enrichment

OUTPUT_DIR = "data/processed"
OUTPUT_FILE = f"{OUTPUT_DIR}/ethiopia_fi_unified_data_enriched.xlsx"
LOG_FILE = "docs/data_enrichment_log.md"


def build_log(new_observations, new_events, new_impact_links):
    lines = ["# Data Enrichment Log\n"]
    lines.append("Documents every record added to the starter dataset during Task 1.\n")

    lines.append("## New Observations\n")
    for rec in new_observations:
        lines.append(f"### {rec['indicator']} ({rec['observation_date']})")
        lines.append(f"- **Value:** {rec['value_numeric']} {rec.get('unit', '')}")
        lines.append(f"- **Pillar:** {rec['pillar']}")
        lines.append(f"- **Source:** [{rec['source_name']}]({rec['source_url']})")
        lines.append(f"- **Original text:** \"{rec['original_text']}\"")
        lines.append(f"- **Confidence:** {rec['confidence']}")
        lines.append(f"- **Collected by:** {rec['collected_by']} on {rec['collection_date']}")
        lines.append(f"- **Why it's useful:** {rec['notes']}\n")

    lines.append("## New Events\n")
    for rec in new_events:
        lines.append(f"### {rec['indicator']} ({rec['observation_date']})")
        lines.append(f"- **Record ID:** {rec['record_id']}")
        lines.append(f"- **Category:** {rec['category']}")
        lines.append(f"- **Source:** [{rec['source_name']}]({rec['source_url']})")
        lines.append(f"- **Original text:** \"{rec['original_text']}\"")
        lines.append(f"- **Confidence:** {rec['confidence']}")
        lines.append(f"- **Collected by:** {rec['collected_by']} on {rec['collection_date']}")
        lines.append(f"- **Why it's useful:** {rec['notes']}\n")

    lines.append("## New Impact Links\n")
    for rec in new_impact_links:
        lines.append(f"### Links {rec['parent_id']} -> {rec['related_indicator']}")
        lines.append(f"- **Pillar:** {rec['pillar']}")
        lines.append(f"- **Direction / Magnitude:** {rec['impact_direction']} / {rec['impact_magnitude']}")
        lines.append(f"- **Lag:** {rec['lag_months']} months")
        lines.append(f"- **Evidence basis:** {rec['evidence_basis']}")
        lines.append(f"- **Confidence:** {rec['confidence']}")
        lines.append(f"- **Collected by:** {rec['collected_by']} on {rec['collection_date']}")
        lines.append(f"- **Why it's useful:** {rec['notes']}\n")

    return "\n".join(lines)


if __name__ == "__main__":

    print("\n STEP 1: LOAD ORIGINAL DATA \n")
    data = data_loader.load_all()
    main_df = data["main"]
    impact_df = data["impact"]

    print("\n STEP 2: GET NEW RESEARCHED RECORDS \n")
    new_observations = build_enrichment.get_new_observations()
    new_events = build_enrichment.get_new_events()
    new_impact_links = build_enrichment.get_new_impact_links()

    print("\n STEP 3: APPEND TO MAIN SHEET \n")
    main_enriched = enrich.append_records(main_df, new_observations + new_events)
    print(f"Main sheet: {len(main_df)} rows -> {len(main_enriched)} rows")

    print("\n STEP 4: APPEND TO IMPACT SHEET \n")
    impact_enriched = enrich.append_records(impact_df, new_impact_links)
    print(f"Impact sheet: {len(impact_df)} rows -> {len(impact_enriched)} rows")

    print("\n STEP 5: SAVE ENRICHED DATASET \n")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with pd.ExcelWriter(OUTPUT_FILE) as writer:
        main_enriched.to_excel(writer, sheet_name="ethiopia_fi_unified_data", index=False)
        impact_enriched.to_excel(writer, sheet_name="Impact_sheet", index=False)
    print(f"Saved enriched dataset to {OUTPUT_FILE}")

    print("\n STEP 6: WRITE ENRICHMENT LOG \n")
    os.makedirs("docs", exist_ok=True)
    log_text = build_log(new_observations, new_events, new_impact_links)
    with open(LOG_FILE, "w") as f:
        f.write(log_text)
    print(f"Saved enrichment log to {LOG_FILE}")