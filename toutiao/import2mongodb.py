import json
import os

import pymongo


def import_to_mongodb():
    my_favorite_files = sorted([f for f in os.listdir('.') if f.startswith('myfavorites-')])
    for file_name in my_favorite_files:
        print(f'------------------------{file_name}')
        with open(file_name, 'r', encoding='utf-8') as f:
            lines = f.readlines()[::-1]
            for line in lines:
                page: dict = json.loads(line)
                records = page['data']
                if records:
                    records = records[::-1]
                    # for r in records:
                    #     print(r)
                    write_to_db(records)


def write_to_db(records):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["myfav"]
    collections = db["toutiao"]
    collections.insert_many(records)
    # x = collections.insert_one(records)
    # print(x.inserted_id)


if __name__ == '__main__':
    import_to_mongodb()
