import os

from pymongo import MongoClient

class MongoConnection:
    db = None
    def __init__(self):
        try:
            connection_host = os.getenv('MONGO_HOST') or 'mongodb://localhost:27017'
            database_name = os.getenv('MONGO_DATABASE') or 'default'
            client = MongoClient(connection_host)
            self.db = client[database_name]
        except Exception as err:
            print('err connect', str(err))
            raise err
            
    def getCollection(self, name):
        return self.db[name]
    