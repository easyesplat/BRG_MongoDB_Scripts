# Get the database using the method we defined in pymongo_test_insert file
def process_hazard_pairs(
    hazard_effect_map: dict, building_specific_map: dict, db
) -> None:
    building_specific_doc_id = insert_to_collection(
        "Buildings", building_specific_map, db
    )
    hazard_effect_doc_id = insert_to_collection("Hazard_Effect", hazard_effect_map, db)
    return hazard_effect_doc_id, building_specific_doc_id


"""
Inserts a document to a specified collection.
Returns the document id for cross-referencing.
"""


def insert_to_collection(collection_name: str, document_map: dict, db) -> str:
    collection = db[collection_name]
    result = collection.insert_one(document_map)
    return result.inserted_id


# if __name__ == "__main__":
# Get the database
# insert_to_collection()
