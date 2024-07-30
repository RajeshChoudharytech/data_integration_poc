from motor.motor_asyncio import AsyncIOMotorClient

MONGO_DETAILS = "mongodb://localhost:27017"

#an asynchronous driver for MongoDB in Python
#designed to work with asyncio,
client = AsyncIOMotorClient(MONGO_DETAILS)
"""
    MongoDB data integration. data_integration is the name of the database you want to use.  
    If the database doesn't exist yet, MongoDB will create it when you first store data in it.
"""
database = client.data_integration

"""
    method retrieves a collection from the specified database. In MongoDB, a collection is a grouping 
    of documents (similar to a table in SQL databases). Here, "sources" is the name of the collection 
    you are accessing. If the collection doesn't exist, MongoDB will create it when you first insert data
    into it.
"""
source_collection = database.get_collection("sources")
