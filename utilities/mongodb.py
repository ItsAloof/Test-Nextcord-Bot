from pymongo import MongoClient
import pymongo
import os

class MongoDB():
    default_database = "guilds"
    default_collection = "settings"
    def __init__(self, connection_url: str):
        self.client = MongoClient(connection_url)
    
    def getClient(self):
        return self.client
    
    def getDatabase(self, database_name: str = default_database):
        return self.client[database_name]
    
    def getCollection(self, database: str = default_database, collection_name: str = default_collection):
        return self.getDatabase(database).get_collection(collection_name)
    
    def insertOne(self, collection_name: str, data):
        return self.getCollection(collection_name).insert_one(data)
    
    def insertMany(self, collection_name: str, data: list):
        return self.getCollection(collection_name).insert_many(data)
    
    def insertGuild(self, collection_name: str = default_collection, guild_id: int = None, data: dict = None):
        return self.getCollection(collection_name=collection_name).insert_one({'guild_id': guild_id, **data})
    
    def findGuild(self, collection_name: str = default_collection, guild_id: int = None):
        if guild_id is None:
            return self.getCollection(collection_name).find_one()
        else:
            return self.getCollection(collection_name).find_one({'guild_id': guild_id})
