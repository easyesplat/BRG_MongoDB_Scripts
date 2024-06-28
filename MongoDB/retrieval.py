from pymongo import MongoClient
from bson import ObjectId
from get_database import get_database
from image_manager import print_image


class HazardDBRetrieval:
    def __init__(self):
        self.hi = 0
    
    # Function to retrieve one document's content(s)
    def retrieve_one_document(self,object_id_str, collection_name, specific_field="all"):
        db = get_database("MultiHazardDatabase")
        collection = db[collection_name]
        document_id = ObjectId(object_id_str)
        document = collection.find_one({"_id": document_id})
        if specific_field == "all":
            print(document)
        else:
            print(document[specific_field])


    def retrieve_one_document(self,collection_name):
        db = get_database("MultiHazardDatabase")
        collection = db[collection_name]
        document = collection.aggregate([{"$sample": {"size": 1}}]).next()
        return document


    def print_one_image():
        document = self.retrieve_one_document("HazardEffects")
        image_ids = document["photos"]
        print_image(image_ids[0])


    def query_db(self, collection_name):
        db = get_database("MultiHazardDatabase")
        collection = db[collection_name]
        # query = {"damage_state": {"$gt": 3}}
        query = {
        "photos": {
            "$exists": True,
            "$ne": []
        }
    }
        documents = collection.find(query)
        # print_image(documents[2]["photos"][0])
        print(collection.count_documents(query))
        # for document in documents:
        #     print(document["roof_cover_damage"])


if __name__ == "__main__":
    # print_one_image()
    query_db("HazardEffects")
