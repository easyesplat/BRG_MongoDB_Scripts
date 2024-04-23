from pymongo import MongoClient
from bson import ObjectId
from get_database import get_database

# Function to retrieve one document's content(s)
def retrieve_one_document(object_id_str, collection_name, specific_field="all"):
    db = get_database("hazards")
    collection = db[collection_name]
    document_id = ObjectId(object_id_str)
    document = collection.find_one({'_id': document_id})
    if specific_field == "all":
        print(document)
    else:
        print(document[specific_field])

  
if __name__ == "__main__":   
    # Get the database
    retrieve_one_document('661c255aa92a28ccbb3a2458', "buildings")