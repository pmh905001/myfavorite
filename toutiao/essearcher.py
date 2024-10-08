import json
import logging

from elastic_transport import ObjectApiResponse
from prettytable import PrettyTable

from es import ES


class ESSearcher(ES):
    SIZE = 10

    def __init__(self, url='http://localhost:9200', index="mytoutiaofav"):
        super().__init__(url, index)

    def query(self, keywords=None, page=1, size=SIZE) -> ObjectApiResponse:
        body = {
            "sort": [{"_score": {"order": "desc"}}, {"increasement_id": {"order": "desc", 'unmapped_type': 'long'}}],
            "from": (page - 1) * size,
            "size": size
        }
        if keywords:
            body.update(
                {
                    "query": {
                        "multi_match": {
                            "query": f"{keywords}",
                            # source means author. weight of title is high
                            "fields": ["title^10", 'abstract', 'source', 'content', 'md_content']
                            # set high weight for full match
                            , "tie_breaker": 0.3
                        },

                    }
                }
            )
        result = self.client.search(index=self.index, body=body, ignore_unavailable=True)
        return result

    def display(self, response):
        hits = response['hits']['hits']
        logging.getLogger().setLevel(logging.INFO)
        table = PrettyTable(['Title', 'Link', 'increasement_id', '_score'])
        for record in hits:
            source = record['_source']
            row = (source['title'], source.get('url', ''), source['increasement_id'], record['_score'])
            table.add_row(row)
        print(table)

    def search(self, keywords, page=1, size=SIZE):
        response = self.query(keywords, page, size)
        self.display(response)
        
        
    def delete(self, id):
        self.client.delete(index=self.index,id=id)


if __name__ == '__main__':
    # ESSearcher().search('python 内存管理')
    # ESSearcher(url='http://192.168.3.185:9200').search('python 内存管理')
    # ESSearcher(url='http://192.168.3.185:9200').search('')
    # ESSearcher().search('', 1, 100)
    # ESSearcher().search('requests', 1, 100)
    
    ESSearcher().delete('requests')
