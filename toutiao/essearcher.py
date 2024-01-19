from elasticsearch import Elasticsearch
from prettytable import PrettyTable


class ESSearcher:

    def __init__(self, url='http://localhost:9200', index="mytoutiaofav"):
        self.url = url
        self.index = index
        self.client = Elasticsearch([self.url])

    def query(self, keywords=None):
        if not keywords:
            return None
        body = {
            "query": {"multi_match": {"query": f"{keywords}", "fields": ["title", 'abstract', 'source']}},
            "sort": [{"_id": {"order": "desc", 'unmapped_type': 'long'}}],
            "size": 20
        }
        result = self.client.search(index=self.index, body=body, ignore_unavailable=True)
        return result

    def display(self, response):
        hits = response['hits']['hits']
        table = PrettyTable(['Title', 'Link', 'abstract'])
        for record in hits:
            source = record['_source']
            row = (source['title'], source.get('url', ''), record['_id'])
            table.add_row(row)
        print(table)

    def search(self, keywords):
        response = self.query(keywords)
        self.display(response)


if __name__ == '__main__':
    ESSearcher().search('图片')
