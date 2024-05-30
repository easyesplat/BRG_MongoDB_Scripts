import pandas as pd
import parsing
import insert
from get_database import get_database


def execute_hurricane_harvey(input_file_name: str):
    data = pd.read_csv(input_file_name)
    rows = len(data.index)
    db = get_database("Hazard")
    hurricane_building_effect_pair = []
    for i in range(rows):
        # Print meant purely for logging purposes.
        print("\033[91mColumn is\033[0m " + str(i))
        row = pd.Series(data.iloc[i]).to_dict()
        hazard_effect_document, building_specific_document = (
            parsing.parse_hurricane_michael(row)
        )
        hazard_effect_id, building_specific_id = insert.process_hazard_pairs(
            hazard_effect_document, building_specific_document, db
        )
        hurricane_building_effect_pair.append(
            {
                "hazard_effect_id:": hazard_effect_id,
                "building_specific_id": building_specific_id,
            }
        )
    insert.insert_to_collection(
        "Hurricanes", {"name": "Michael", "pairs": hurricane_building_effect_pair}, db
    )


def execute_hurricane_laura(input_file_name: str):
    data = pd.read_csv(input_file_name)
    rows = len(data.index)
    db = get_database("Hazard")
    hurricane_building_effect_pair = []
    for i in range(rows):
        # Print meant purely for logging purposes.
        print("\033[91mColumn is\033[0m " + str(i))
        row = pd.Series(data.iloc[i]).to_dict()
        hazard_effect_document, building_specific_document = (
            parsing.parse_hurricane_laura(row)
        )
        hazard_effect_id, building_specific_id = insert.process_hazard_pairs(
            hazard_effect_document, building_specific_document, db
        )
        hurricane_building_effect_pair.append(
            {
                "hazard_effect_id:": hazard_effect_id,
                "building_specific_id": building_specific_id,
            }
        )
    insert.insert_to_collection(
        "Hurricanes", {"name": "Laura", "pairs": hurricane_building_effect_pair}, db
    )

def execute_hurricane_dorian(input_file_name: str):
    data = pd.read_excel(input_file_name)
    rows = len(data.index)
    db = get_database("Hazard")
    hurricane_building_effect_pair = []
    for i in range(rows):
        # Print meant purely for logging purposes.
        print("\033[91mColumn is\033[0m " + str(i))
        row = pd.Series(data.iloc[i]).to_dict()
        hazard_effect_document, building_specific_document = (
            parsing.parse_hurricane_dorian(row)
        )
        hazard_effect_id, building_specific_id = insert.process_hazard_pairs(
            hazard_effect_document, building_specific_document, db
        )
        hurricane_building_effect_pair.append(
            {
                "hazard_effect_id:": hazard_effect_id,
                "building_specific_id": building_specific_id,
            }
        )
    insert.insert_to_collection(
        "Hurricanes", {"name": "Dorian", "pairs": hurricane_building_effect_pair}, db
    )


if __name__ == "__main__":
    # execute_hurricane_harvey("../Data/Hurricane_Michael/HM_D2D_Building.csv")
    # execute_hurricane_laura("../Data/Hurricane_Laura/HL_D2D_Building.csv")
    execute_hurricane_dorian("../Data/Hurricane_Dorian/Dorian_PA_Final.xlsx")
