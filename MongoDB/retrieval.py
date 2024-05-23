from pymongo import MongoClient
from bson import ObjectId
from get_database import get_database
from image_manager import print_image

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

def retrieve_one_document(collection_name):
    db = get_database("hazards")
    collection = db[collection_name]
    document = collection.aggregate([{'$sample': {'size': 1}}]).next()
    return document

def print_one_image():
    document = retrieve_one_document("hazard_effect")
    image_ids = document["photo"]
    print_image(image_ids[0])
  
if __name__ == "__main__":   
    print_one_image()