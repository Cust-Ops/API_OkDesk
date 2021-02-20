from pymongo import MongoClient
from config import DB_URL, token
import requests
import json


class OkDesk:
    """ Connection to cirex.okdesk.ru and take "Open Issue" from client """
    def __init__(self, token):
        self.token = token

    def connection_db(self):
        """ Connection to DataBase """
        client = MongoClient(DB_URL)
        db = client.testDB
        collection = db.okdesktt
        return collection

    def ok_request(self):
        """ Return list id issue and insert with open status in DB"""
        req = requests.get(f'https://cirextp.okdesk.ru/api/v1/issues/count?api_token={self.token}')
        json_req = json.loads(req.text)
        for id_tt in json_req:
            stat_req = requests.get(f'https://cirextp.okdesk.ru/api/v1/issues/{id_tt}?api_token={self.token}')
            json_stat = json.loads(stat_req.text)
            if json_stat['status']['name'] == 'Открыта':
                try:
                    self.connection_db().insert_one(json_stat)
                except EOFError:
                    print("Could not connect to MongoDB")
                finally:
                    print('Data insert')

    def count_tt(self):
        sum_tt = 0
        for x in self.connection_db().find({}, {'status': {'name': 'Открыта'}}):
            sum_tt += 1
        return sum_tt

    def get_link(self):
        for link in self.connection_db().find({}, {'id'}):
            return f'https://cirextp.okdesk.ru/issues/{link["id"]}'


test = OkDesk(token)
test.get_link()
