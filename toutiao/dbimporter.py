import json
import os


class DBImporter:

    def import_to_db(self):
        last_id = self.find_last_id_from_db()
        my_favorite_files = self.get_my_favorites_files(last_id)
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
                        self.write_to_db(records)

    def get_my_favorites_files(self, last_id):
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

    def find_last_id_from_db(self):
        raise NotImplementedError('not implement yet!')

    def write_to_db(self, records):
        raise NotImplementedError('not implement yet!')
