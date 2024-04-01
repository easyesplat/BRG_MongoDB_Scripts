import pandas as pd
from insert import process_hurricane_harvey

def parse_csv_file(input_file_name: str):
    data = pd.read_csv(input_file_name)
    rows = len(data.index)
    for i in range(1):
        row = pd.Series(data.iloc[i]).to_dict()
        hazard_effect_document = {
            "damage_state": row["status"],
            "date": row["date"],
            "assessment_type": row["assessment_type"],
            "photo": row["all_photos"],
            "photo_caption": row["all_photos_caption"],
            "surveyor_notes": row["general_notes"],
            "hazards_present": row["hazards_present"],
            "wind_damage_rating": row["wind_damage_rating"]
        }
        housing_document = {
            "latitude": row['latitude'],
            "longitude": row["longitude"],
        }
        process_hurricane_harvey(housing_document, hazard_effect_document)


if __name__ == "__main__":
    parse_csv_file("../Data/Hurricane_Michael/HM_D2D_Building.csv")