import json
import sqlite3

from toutiao.dbimporter import DBImporter


class SqliteImporter(DBImporter):

    def __init__(self, db='../myfav.db'):
        self.db = db

    def find_last_id_from_db(self):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT info FROM toutiao ORDER BY id DESC LIMIT 1')
            record = cursor.fetchone()
            if record:
                last_id = json.loads(record[0])['id']
            cursor.close()
        return last_id

    def write_to_db(self, records):
        if not records:
            return
        records = [json.dumps(r, ensure_ascii=False) for r in records]
        with sqlite3.connect(self.db) as conn:
            sql = f'INSERT INTO toutiao (info) VALUES {",".join(["(?)"] * len(records))}'
            conn.execute(sql, records)
            conn.commit()


if __name__ == '__main__':
    SqliteImporter().import_to_db()
