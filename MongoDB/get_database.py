from pymongo import MongoClient
from constant import USERNAME, PASSWORD

"""
Remember to create your own constant.py file and include your own MongoDB username and password.
"""


def get_database(db_name: str):

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = f"mongodb+srv://{USERNAME}:{PASSWORD}@serverlessinstance0.6essvcc.mongodb.net/?retryWrites=true&w=majority&appName=ServerlessInstance0"
    # CONNECTION_STRING = f"mongodb+srv://{USERNAME}:{PASSWORD}@hazard.do2ugno.mongodb.net/?retryWrites=true&w=majority&appName=Hazard"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)
    return client[db_name]


# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":

    # Get the database
    dbname = get_database("MultiHazardDatabase")
    print(dbname)
