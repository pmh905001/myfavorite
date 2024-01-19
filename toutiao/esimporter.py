import json
import logging

from elastic_transport import ObjectApiResponse

from toutiao.dbimporter import DBImporter
from elasticsearch import Elasticsearch


class ESImporter(DBImporter):
    def __init__(self, url='http://localhost:9200', index="mytoutiaofav"):
        self.url = url
        self.index = index
        self.client = Elasticsearch([self.url])

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

    def write_to_db(self, records):
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


if __name__ == '__main__':
    # ESImporter().find_last_id_from_db()
    ESImporter().import_to_db()
