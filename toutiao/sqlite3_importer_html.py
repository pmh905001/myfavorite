import json
import logging
import os
import sqlite3

from converter import convert_html_to_markdown
from dbimporter import DBImporter
import logging

from log import Log


class Sqlite3ImporterFromHTMLContent(DBImporter):
    def __init__(self, db='../myfav.db'):
        self.db = db
    
    def find_last_id_from_db(self):
        last_id=None
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT info FROM toutiao WHERE md_content is not null ORDER BY id DESC LIMIT 1')
            record = cursor.fetchone()
            if record:
                last_id = json.loads(record[0])['id']
            cursor.close()
        return last_id

    def _files(self):
        return sorted([f for f in os.listdir('files') if f.startswith('htmlcontent-myfavorites-')])

    def _locate_position(self, files, last_id):
        if not last_id:
            return [(f, -1, -1) for f in files]
        # reverse files to find out position fast.
        files = sorted(files, reverse=True)
        result = []
        for file in files:
            with open(f'files/{file}', 'r', encoding='utf-8') as f:
                for line_number, line in enumerate(f):
                    page = json.loads(line)
                    if last_id in page:
                        if not line_number == 0:
                            result.append((file, line_number, -1))
                        return result[::-1]
                result.append((file, -1, -1))
        raise FileNotFoundError(f'not found files by id: {last_id}')
    
    def import_to_db(self):
        last_id = self.find_last_id_from_db()
        files = self._files()
        my_favorite_files = self._locate_position(files, last_id)
        for file_name, line_number, record_number in my_favorite_files:
            logging.info(f'------------------------{file_name}')
            with open(f'files/{file_name}', 'r', encoding='utf-8') as f:
                lines = f.readlines()[::-1]
                if line_number != -1:
                    lines = lines[-line_number:]
                id_md_map = {}
                records = []
                for line in lines:
                    id, html_content = json.loads(line).popitem()
                    md_content = convert_html_to_markdown(html_content)
                    logging.info(f'------{id}')
                    id_md_map[id] = md_content
                    records.append({'id': id, 'html': html_content})

                self.write_to_db(id_md_map)
                logging.info(f'update md content for {file_name} success!')
                
    def write_to_db(self, id_content_map: dict):
        data=[(content,id) for id,content in id_content_map.items()]
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            sql="UPDATE toutiao SET md_content=? where json_extract(info,'$.id')=?"
            cursor.executemany(sql,data)
            conn.commit
            cursor.close()
        

if __name__ == '__main__':
    Log.setup()
    Sqlite3ImporterFromHTMLContent().import_to_db()
