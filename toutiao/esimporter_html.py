import json
import logging
import os

from elastic_transport import ObjectApiResponse
from elasticsearch import Elasticsearch
from elasticsearch import helpers

from converter import convert_html_to_markdown
from dbimporter import DBImporter
from es import ES
import logging

from log import Log


class ESImporterFromHTMLContent(ES, DBImporter):
    def __init__(self, url='http://localhost:9200', index="mytoutiaofav"):
        super().__init__(url, index)

        hits = self.get_last_record(self.client, index)['hits']['hits']
        self.increasement_id = hits[0]['_source']['increasement_id'] if hits else 0

        self.id = hits[0]['_source']['id'] if hits else None

    @staticmethod
    def get_last_record(client: Elasticsearch, index):
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "exists": {
                                "field": "md_content"
                            }
                        }
                    ]
                }
            },
            "sort": [
                {
                    "increasement_id": {
                        "order": "desc"
                    }
                }
            ],
            "size": 1
        }
        result: ObjectApiResponse = client.search(index=index, body=body, ignore_unavailable=True)
        return result

    def find_last_id_from_db(self):
        return self.id

    def write_to_db_one_by_one(self, records):
        for record in records:
            self.increasement_id += 1
            logging.info(f"------------------------increasement_id:{self.increasement_id}")
            record['increasement_id'] = self.increasement_id
            if 'content' in record and not isinstance(record['content'], str):
                record['content'] = json.dumps(record['content'], ensure_ascii=False)
            try:
                self.client.index(index=self.index, body=record)
            except:
                logging.exception(f'ignore this error record\n:{json.dumps(record, indent=4, ensure_ascii=False)}')

    def get_ids_by_names(self, ids):
        query = {
            "_source": ["id"],
            "query": {
                "terms": {
                    "id.keyword": ids
                }
            }
        }
        response = self.client.search(index=self.index, body=query, size=len(ids))
        hits = response['hits']['hits']
        return {hit['_source']['id']: hit['_id'] for hit in hits}

    def generate_update_actions(self, id_content_map, id_to_index_id_map):
        
        for id, _id in id_to_index_id_map.items():
            content=id_content_map.get(id)
            if _id and content :
                yield {
                    "_op_type": "update",
                    "_index": self.index,
                    "_id": _id,
                    "doc": {"md_content": content}
                }
            else:
                logging.info(f"Document with id={id} not found")

    def write_to_db(self, id_content_map: dict):
        
        ids=list(id_content_map.keys())
        
        while len(ids)>0:
            section = ids[:100]
            logging.info(f'search index id according 100 ids:{section}')
            items = self.get_ids_by_names(section)
            logging.info(f'search result:{items}')
            del ids[:100]
        
            actions = self.generate_update_actions(id_content_map, items)
            actions = [action for action in actions if action]
        
            logging.info(f'start to update {len(actions)} records')
            helpers.bulk(self.client, actions)
            logging.info(f'end to update')

    def write_to_db_for_html_content(self, records):
        records_to_insert = []
        for record in records:
            records_to_insert.append(
                {
                    "_index": 'mytoutiaofav_html',
                    "_source": record
                }
            )
        
        helpers.bulk(self.client, records_to_insert)

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
                # self.write_to_db_for_html_content()
                # logging.info(f'update html content for {file_name} success!')

if __name__ == '__main__':
    Log.setup()
    ESImporterFromHTMLContent().import_to_db()
