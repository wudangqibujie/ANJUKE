import pymongo

class Data2Mongo(object):
    def __init__(self,db_name):
        self.client = pymongo.MongoClient("localhost",port=27017)
        self.db = self.client[db_name]
    def insert_data(self,coll_name,data):
        coll = self.db[coll_name]
        coll.insert(data)
