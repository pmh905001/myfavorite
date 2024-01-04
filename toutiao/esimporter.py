import json
import logging

from toutiao.dbimporter import DBImporter
from elasticsearch import Elasticsearch


class ESImporter(DBImporter):
    def __init__(self, url='http://localhost:9200', index="mytoutiaofav"):
        self.url = url
        self.index = index
        self.client = Elasticsearch([self.url])
        hits = self.get_last_record(self.client, index)['hits']['hits']
        self._id = int(hits[0]['_id']) if hits else 0
        self.id = hits[0]['_source']['id'] if hits else None

    @staticmethod
    def get_last_record(client: Elasticsearch, index):
        body = {
            "query": {"match_all": {}},
            "sort": [{"_id": {"order": "desc", 'unmapped_type': 'long'}}],
            "size": 1
        }
        result = client.search(index=index, body=body, ignore_unavailable=True)
        return result

    def find_last_id_from_db(self):
        return self.id

    def write_to_db(self, records):
        for record in records:
            self._id += 1
            print(f"------------------------_id:{self._id}")
            if 'content' in record:
                del record['content']
            try:
                self.client.index(index=self.index, body=record, id=self._id)
                if 'content' in record:
                    logging.warning(f'record\n:{json.dumps(record, indent=4, ensure_ascii=False)}')
            except:
                logging.exception(f'ignore this error record\n:{json.dumps(record,indent=4,ensure_ascii=False)}')


if __name__ == '__main__':
    # # 创建 Elasticsearch 客户端
    # client = Elasticsearch(["http://localhost:9200"])
    #
    # # 定义要写入的数据
    # data = {
    #     "field1": "value111",
    #     "field2": "value222"
    # }
    #
    # # 写入数据到指定索引和文档类型
    # client.index(index="my_index", body=data, id=1)

    # ESImporter().find_last_id_from_db()
    ESImporter().import_to_db()
