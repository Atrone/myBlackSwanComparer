import pymongo
import random

class MyMongo:
    def __init__(self,client_string:str=""):
        self.client = pymongo.MongoClient(client_string)

    def check_if_key_exists(self,db_name,col_name,key_name,key_value):
        db = self.client[db_name]
        col = db[col_name]
        if (col.find_one({key_name:key_value})):
            return True
        return False

    def insert_values_under_key(self,db_name,col_name,value_name,list_of_value_values,key_name,key_value):
        db = self.client[db_name]
        col = db[col_name]
        for value_value in list_of_value_values:
            col.insert_one({key_name:key_value,value_name:value_value})

    def get_random_doc(self,db_name,col_name,key_name,key_value,value_name):
        db = self.client[db_name]
        col = db[col_name]
        count = col.count()
        agg = col.aggregate([{"$match":{key_name:key_value}},{"$sample":{'size':1}}])
        results = []
        for a in agg:
            results.append(a[value_name])
        return results
    
    def run_aggregation(self, db_name, col_name, query):
        db = self.client[db_name]
        col = db[col_name]
        agg = col.aggregate(query)
        return agg

