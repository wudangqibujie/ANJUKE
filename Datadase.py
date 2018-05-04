import pymongo

class Data2Mongo(object):
    def __init__(self,db_name):
        self.client = pymongo.MongoClient("localhost",port=27017)
        self.db = self.client[db_name]
    def insert_data(self,coll_name,data):
        coll = self.db[coll_name]
        coll.insert(data)
    def find_city_url(self,city_name):
        coll = self.db["city_urls"]
        a = coll.find_one({city_name:{"$regex":".*"}})
        return  a[city_name]
if __name__ == '__main__':
    d = Data2Mongo("anjuke")
    want_city = ["北京","上海","广州","深圳"]
    city_urls = [d.find_city_url(i) for i in want_city]
    print(city_urls)