import pymongo

from toutiao.dbimporter import DBImporter


class MongoDBImporter(DBImporter):
    def __init__(self, db='mongodb://localhost:27017/'):
        self.db = db

    def find_last_id_from_db(self):
        client = pymongo.MongoClient(self.db)
        db = client["myfav"]
        collections = db["toutiao"]
        record = collections.find().sort({'_id': -1}).limit(1).next()
        return record['id'] if record else None

    def write_to_db(self, records):
        client = pymongo.MongoClient(self.db)
        db = client["myfav"]
        collections = db["toutiao"]
        collections.insert_many(records)
        # x = collections.insert_one(records)
        # print(x.inserted_id)


if __name__ == '__main__':
    MongoDBImporter().import_to_db()
