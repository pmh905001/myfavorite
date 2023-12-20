import json
import os

import pymongo


def import_to_mongodb():
    last_id = find_last_id_from_db()
    my_favorite_files = get_my_favorites_files(last_id)
    for file_name, pos in my_favorite_files:
        print(f'------------------------{file_name}')
        with open(file_name, 'r', encoding='utf-8') as f:
            lines = f.readlines()[::-1]
            if pos != -1:
                lines = lines[-pos:]
            for line in lines:
                page: dict = json.loads(line)
                records = page['data']
                if records:
                    records = records[::-1]
                    write_to_db(records)


def get_my_favorites_files(last_id):
    files = sorted([f for f in os.listdir('.') if f.startswith('myfavorites-')])
    if not last_id:
        return [(f, -1) for f in files]
    files = sorted(files, reverse=True)
    result = []
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                page = json.loads(line)
                if page['data']:
                    for index, record in enumerate(page['data']):
                        if record['id'] == last_id:
                            if index != 0:
                                result.append((file, index))
                            return result[::-1]
            result.append((file, -1))
    raise FileNotFoundError(f'not found files by id: {last_id}')


def find_last_id_from_db():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["myfav"]
    collections = db["toutiao"]
    record = collections.find().sort({'_id': -1}).limit(1).next()
    return record['id'] if record else None


def write_to_db(records):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["myfav"]
    collections = db["toutiao"]
    collections.insert_many(records)
    # x = collections.insert_one(records)
    # print(x.inserted_id)


if __name__ == '__main__':
    import_to_mongodb()
