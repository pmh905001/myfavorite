import json
import logging

from elastic_transport import ObjectApiResponse

from toutiao.dbimporter import DBImporter
from elasticsearch import Elasticsearch


class ESImporter(DBImporter):
    def __init__(self, url='http://localhost:9200', index="mytoutiaofav"):
        self.url = url
        self.index = index
        self.client = Elasticsearch([self.url], request_timeout=60, max_retries=10, retry_on_timeout=True)

        hits = self.get_last_record(self.client, index)['hits']['hits']
        self.increasement_id = hits[0]['_source']['increasement_id'] if hits else 0

        self.id = hits[0]['_source']['id'] if hits else None

    @staticmethod
    def get_last_record(client: Elasticsearch, index):
        body = {
            "query": {"match_all": {}},
            "sort": [{"increasement_id": {"order": "desc", 'unmapped_type': 'long'}}],
            "size": 1
        }
        result: ObjectApiResponse = client.search(index=index, body=body, ignore_unavailable=True)
        # if result.raw['hits']['hits']:
        #     logging.warning(f'jump this record\n:{json.dumps(result.raw, indent=4, ensure_ascii=False)}')
        return result

    def find_last_id_from_db(self):
        return self.id

    def write_to_db_one_by_one(self, records):
        for record in records:
            self.increasement_id += 1
            print(f"------------------------increasement_id:{self.increasement_id}")
            record['increasement_id'] = self.increasement_id
            if 'content' in record and not isinstance(record['content'], str):
                record['content'] = json.dumps(record['content'], ensure_ascii=False)
            try:
                self.client.index(index=self.index, body=record)
            except:
                logging.exception(f'ignore this error record\n:{json.dumps(record, indent=4, ensure_ascii=False)}')

    def write_to_db(self, records):
        records_to_insert = []
        for record in records:
            self.increasement_id += 1
            print(f"------------------------increasement_id:{self.increasement_id}")
            record['increasement_id'] = self.increasement_id
            if 'content' in record and not isinstance(record['content'], str):
                record['content'] = json.dumps(record['content'], ensure_ascii=False)
            records_to_insert.append(
                {
                    "_index": self.index,
                    "_source": record
                }
            )
        from elasticsearch import helpers
        helpers.bulk(self.client, records_to_insert)

    def import_to_db(self):
        last_id = self.find_last_id_from_db()
        files = self._files()
        my_favorite_files = self._locate_position(files, last_id)
        for file_name, line_number, record_number in my_favorite_files:
            print(f'------------------------{file_name}')
            with open(file_name, 'r', encoding='utf-8') as f:
                lines = f.readlines()[::-1]
                if line_number != -1:
                    lines = lines[-line_number:]
                total_records = []
                for line in lines:
                    page: dict = json.loads(line)
                    records = page['data']
                    if records:
                        records = records[::-1]
                        if record_number != -1:
                            records = records[-record_number:]
                    total_records.extend(records)
                self.write_to_db(total_records)


if __name__ == '__main__':
    # ESImporter().import_to_db()
    ESImporter(url='http://192.168.3.185:9200').import_to_db()
