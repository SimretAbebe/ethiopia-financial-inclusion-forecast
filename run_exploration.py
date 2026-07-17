from src import data_loader
from src import data_explorer
from src import data_validator

if __name__ == "__main__":

    print("\n########## STEP 1: LOADING DATA ##########\n")
    data = data_loader.load_all()
    main_df = data["main"]
    impact_df = data["impact"]
    reference_df = data["reference"]

    print("\n########## STEP 2: VALIDATING AGAINST REFERENCE CODES ##########\n")
    data_validator.validate_all(main_df, reference_df)

    print("\n########## STEP 3: EXPLORING MAIN SHEET ##########\n")
    data_explorer.summarize(main_df)

    print("\n########## STEP 4: IMPACT LINK OVERVIEW ##########\n")
    print(f"Total impact_links: {len(impact_df)}")
    print("\nImpact links grouped by pillar affected:")
    print(data_explorer.count_by_column(impact_df, "pillar"))
    print("\nImpact links grouped by evidence basis:")
    print(data_explorer.count_by_column(impact_df, "evidence_basis"))