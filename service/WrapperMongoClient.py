from pymongo import MongoClient

class WrapperMongoClient:
    def __init__(self, db="api-cv-ocr",host="mongodb",user="root",password="root", port="27017"):
        uri ="mongodb://"+user+":"+password+"@"+ host+":"+ port
        client = MongoClient(uri)
        self.db = client[db]
    def save(self,table, data):
        self.db[table].insert_one(data)
    def list(self,table):
        return list(self.db[table].find({}))