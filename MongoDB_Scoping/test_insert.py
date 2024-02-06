# Get the database using the method we defined in pymongo_test_insert file
from get_database import get_database

def insert_to_collection(collection_name):
    dbname = get_database("hazards")
    collection_name = dbname["buildings"]

    # sample document inserts
    item_1 = {
    "_id" : "U1IT00001",
    "age": 12,
    "description": "old and burly"
    }

    item_2 = {
    "_id" : "U1IT00002",
    "age": 16,
    "description": "old and burly"
    }
    collection_name.insert_many([item_1,item_2])
  
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   
    # Get the database
    dbname = get_database("hazards")