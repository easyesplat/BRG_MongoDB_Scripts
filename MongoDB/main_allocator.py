import pandas as pd
import parsing
import insert
from get_database import get_database


class DatabaseExecutor:
    def __init__(self, write_privilege=False):
        self.write_privilege = write_privilege
        self.hazard_paths = {
            "hurricane_michael": "../Data/Hurricane_Michael/HM_D2D_Building.csv",
            "hurricane_laura": "../Data/Hurricane_Laura/HL_D2D_Building.csv",
            "hurricane_harvey": "../Data/Hurricane_Harvey/HH-DA.csv",
            "hurricane_dorian": "../Data/Hurricane_Dorian/Dorian_PA_Final.xlsx",
            "earthquake_napa": "../Data/Earthquake_Napa/Napa_Dataset.xlsx",
        }
        self.parser = parsing.EventParser(self.write_privilege)

    def execute_hurricane_michael(self):
        data = pd.read_csv(self.hazard_paths["hurricane_michael"])
        rows = len(data.index)
        db = get_database("MultiHazardDatabase")
        hurricane_building_effect_pair = []
        for i in range(rows):
            # Print meant purely for logging purposes.
            print("\033[91mColumn is\033[0m " + str(i))
            row = pd.Series(data.iloc[i]).to_dict()
            hazard_effect_document, building_specific_document = (
                self.parser.parse_hurricane_michael(row)
            )
            if self.write_privilege:
                hazard_effect_id, building_specific_id = (
                    insert.process_hazard_pairs(
                        hazard_effect_document, building_specific_document, db
                    )
                )
                hurricane_building_effect_pair.append(
                    {
                        "hazard_effect_id:": hazard_effect_id,
                        "building_specific_id": building_specific_id,
                    }
                )
        if self.write_privilege:
            insert.insert_to_collection(
                "Hurricanes",
                {"name": "Michael", "pairs": hurricane_building_effect_pair},
                db,
            )

    def execute_hurricane_laura(self):
        data = pd.read_csv(self.hazard_paths["hurricane_laura"])
        rows = len(data.index)
        db = get_database("MultiHazardDatabase")
        hurricane_building_effect_pair = []
        for i in range(rows):
            # Print meant purely for logging purposes.
            print("\033[91mColumn is\033[0m " + str(i))
            row = pd.Series(data.iloc[i]).to_dict()
            hazard_effect_document, building_specific_document = (
                self.parser.parse_hurricane_laura(row)
            )
            if self.write_privilege:
                hazard_effect_id, building_specific_id = (
                    insert.process_hazard_pairs(
                        hazard_effect_document, building_specific_document, db
                    )
                )
                hurricane_building_effect_pair.append(
                    {
                        "hazard_effect_id:": hazard_effect_id,
                        "building_specific_id": building_specific_id,
                    }
                )
        if self.write_privilege:
            insert.insert_to_collection(
                "Hurricanes",
                {"name": "Laura", "pairs": hurricane_building_effect_pair},
                db,
            )

    def execute_hurricane_harvey(self):
        data = pd.read_csv(self.hazard_paths["hurricane_harvey"])
        rows = len(data.index)
        db = get_database("MultiHazardDatabase")
        hurricane_building_effect_pair = []
        for i in range(rows):
            # Print meant purely for logging purposes.
            print("\033[91mColumn is\033[0m " + str(i))
            row = pd.Series(data.iloc[i]).to_dict()
            hazard_effect_document, building_specific_document = (
                self.parser.parse_hurricane_harvey(row)
            )
            if self.write_privilege:
                hazard_effect_id, building_specific_id = (
                    insert.process_hazard_pairs(
                        hazard_effect_document, building_specific_document, db
                    )
                )
                hurricane_building_effect_pair.append(
                    {
                        "hazard_effect_id:": hazard_effect_id,
                        "building_specific_id": building_specific_id,
                    }
                )
        if self.write_privilege:
            insert.insert_to_collection(
                "Hurricanes",
                {"name": "Harvey", "pairs": hurricane_building_effect_pair},
                db,
            )

    def execute_hurricane_dorian(self):
        data = pd.read_excel(self.hazard_paths["hurricane_dorian"])
        rows = len(data.index)
        db = get_database("MultiHazardDatabase")
        hurricane_building_effect_pair = []
        for i in range(rows):
            # Print meant purely for logging purposes.
            print("\033[91mColumn is\033[0m " + str(i))
            row = pd.Series(data.iloc[i]).to_dict()
            hazard_effect_document, building_specific_document = (
                self.parser.parse_hurricane_dorian(row)
            )
            if self.write_privilege:
                hazard_effect_id, building_specific_id = (
                    insert.process_hazard_pairs(
                        hazard_effect_document, building_specific_document, db
                    )
                )
                hurricane_building_effect_pair.append(
                    {
                        "hazard_effect_id:": hazard_effect_id,
                        "building_specific_id": building_specific_id,
                    }
                )
        if self.write_privilege:
            insert.insert_to_collection(
                "Hurricanes",
                {"name": "Dorian", "pairs": hurricane_building_effect_pair},
                db,
            )

    def execute_earthquake_napa(self):
        data = pd.read_excel(self.hazard_paths["earthquake_napa"], header=1)
        rows = len(data.index)
        db = get_database("MultiHazardDatabase")
        earthquake_building_effect_pair = []
        for i in range(rows):
            print("\033[91mColumn is\033[0m " + str(i))
            row = pd.Series(data.iloc[i]).to_dict()
            hazard_effect_document, building_specific_document = (
                self.parser.parse_earthquake_napa(row)
            )
            if self.write_privilege:
                hazard_effect_id, building_specific_id = insert.process_hazard_pairs(
                    hazard_effect_document, building_specific_document, db
                )
                earthquake_building_effect_pair.append(
                    {
                        "hazard_effect_id:": hazard_effect_id,
                        "building_specific_id": building_specific_id,
                    }
                )
        if self.write_privilege:
            insert.insert_to_collection(
                "Earthquakes",
                {"name": "Napa", "pairs": earthquake_building_effect_pair},
                db,
            )


if __name__ == "__main__":
    database_executor = DatabaseExecutor(write_privilege=False)
    # database_executor.execute_hurricane_michael()
    # database_executor.execute_hurricane_dorian()
    # database_executor.execute_hurricane_harvey()
    # database_executor.execute_hurricane_laura()
    # database_executor.execute_earthquake_napa()
