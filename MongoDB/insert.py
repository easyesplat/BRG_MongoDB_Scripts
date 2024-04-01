# Get the database using the method we defined in pymongo_test_insert file
from get_database import get_database

# Tester Hurricane Harvey Code
def process_hurricane_harvey(building_specific_map: dict, hazard_effect_map: dict) -> None:
    building_specific_doc_id = insert_to_collection("buildings", building_specific_map)
    hazard_effect_doc_id = insert_to_collection("hazard_effect", hazard_effect_map)


# TODO(@easyesplat): Pull get_database() out of insert_to_collection() for efficiency-reasons.
'''
Inserts a document to a specified collection.
Returns the document id for cross-referencing.
'''
def insert_to_collection(collection_name: str, document_map: dict) -> str:
    db = get_database("hazards")
    collection = db[collection_name]
    result = collection.insert_one(document_map)
    return result.inserted_id
  
if __name__ == "__main__":   
    # Get the database
    insert_to_collection()