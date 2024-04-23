import pandas as pd
from parsing import parse_hurricane_michael
from insert import process_hurricane_harvey, insert_to_collection
from get_database import get_database


def execute_hurricane_harvey(input_file_name: str):
    data = pd.read_csv(input_file_name)
    rows = len(data.index)
    db = get_database("hazards")
    hurricane_building_effect_pair = []
    for i in range(rows):
        print("\033[91mColumn is\033[0m" + str(i))
        row = pd.Series(data.iloc[i]).to_dict()
        hazard_effect_document, building_specific_document = parse_hurricane_michael(
            row)
        hazard_effect_id, building_specific_id = process_hurricane_harvey(
            hazard_effect_document, building_specific_document, db)
        hurricane_building_effect_pair.append({
            "hazard_effect_id:":
            hazard_effect_id,
            "building_specific_id":
            building_specific_id
        })
    insert_to_collection("hurricanes", {
                         "name": "Michael", "pairs": hurricane_building_effect_pair }, db)


if __name__ == "__main__":
    # Get the database
    execute_hurricane_harvey("../Data/Hurricane_Michael/HM_D2D_Building.csv")
