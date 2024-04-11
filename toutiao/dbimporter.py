import json
import os


class DBImporter:

    def import_to_db(self):
        last_id = self.find_last_id_from_db()
        files = self._files()
        my_favorite_files = self._locate_position(files, last_id)
        for file_name, line_number, record_number in my_favorite_files:
            print(f'------------------------{file_name}')
            with open(f'files/{file_name}', 'r', encoding='utf-8') as f:
                lines = f.readlines()[::-1]
                if line_number != -1:
                    lines = lines[-line_number:]
                for line in lines:
                    page: dict = json.loads(line)
                    records = page['data']
                    if records:
                        records = records[::-1]
                        if record_number != -1:
                            records = records[-record_number:]
                        self.write_to_db(records)

    def _files(self):
        return sorted([f for f in os.listdir('files') if f.startswith('myfavorites-')])

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
                    if page['data']:
                        for record_number, record in enumerate(page['data']):
                            if record['id'] == last_id:
                                if not (line_number == 0 and record_number == 0):
                                    result.append((file, line_number, record_number))
                                return result[::-1]
                result.append((file, -1, -1))
        raise FileNotFoundError(f'not found files by id: {last_id}')

    def find_last_id_from_db(self):
        raise NotImplementedError('not implement yet!')

    def write_to_db(self, records):
        raise NotImplementedError('not implement yet!')
