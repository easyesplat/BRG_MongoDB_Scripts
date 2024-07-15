from pymongo import MongoClient
from bson import ObjectId
from get_database import get_database
from image_manager import print_image
import pandas as pd
import os


class HazardDBRetrieval:
    def __init__(self):
        self.db = get_database("MultiHazardDatabase")

    def print_one_image(self):
        document = self.retrieve_one_document("HazardEffects")
        image_ids = document["photos"]
        print_image(image_ids[0])

    def query_db(self, query, collection_name):
        collection = self.db[collection_name]
        return collection.find(query)

    def retrieve_csv_from_query(self, query, collection_name, file_path=""):
        documents = self.query_db(query, collection_name)
        df = pd.DataFrame(documents)
        path = file_path
        if file_path == "":
            path = str(os.path.expanduser("~")) + "/output.csv"
        df.to_csv(path, index=False)

    def query_with_building_and_effects(
        self, is_hurricane_hazard, hazard_effect_query, building_query
    ):
        hazards_collection = None
        if is_hurricane_hazard:
            hazards_collection = self.db["Hurricanes"]
        else:
            hazards_collection = self.db["Earthquakes"]
        hazard_effects_collection = self.db["HazardEffects"]
        buildings_collection = self.db["Buildings"]

        hazard_effects_cursor = hazard_effects_collection.find(hazard_effect_query)
        hazard_effects_ids = {ObjectId(doc["_id"]) for doc in hazard_effects_cursor}

        buildings_cursor = buildings_collection.find(building_query)
        buildings_ids = {ObjectId(doc["_id"]) for doc in buildings_cursor}

        pipeline = [
            {"$unwind": "$pairs"},
            {
                "$match": {
                    "pairs.hazard_effect_id:": {"$in": list(hazard_effects_ids)},
                    "pairs.building_specific_id": {"$in": list(buildings_ids)},
                }
            },
            {"$project": {"_id": 0, "pairs": 1}},
        ]

        matching_pairs = hazards_collection.aggregate(pipeline)
        matching_pairs_list = [
            matching_pair["pairs"] for matching_pair in matching_pairs
        ]
        return matching_pairs_list


if __name__ == "__main__":
    retrieval = HazardDBRetrieval()
    # query = {"photos": {"$exists": True, "$ne": []}}
    # retrieval.retrieve_csv_from_query(query, "HazardEffects", "Data_Exploration/output.csv")
    retrieval.query_with_building_and_effects(
        True,
        {"damage_state": {"$gte": 4}},
        {"hazard_event": {"$eq": "Hurricane Michael"}},
    )
