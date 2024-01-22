from prettytable import PrettyTable

from toutiao.es import ES


class ESSearcher(ES):

    def __init__(self, url='http://localhost:9200', index="mytoutiaofav"):
        super().__init__(url, index)

    def query(self, keywords=None):
        if not keywords:
            return None
        body = {
            # source means author.
            "query": {"multi_match": {"query": f"{keywords}", "fields": ["title", 'abstract', 'source', 'content']}},
            # "query": {"multi_match": {"query": f"{keywords}", "fields": ["title"]}},
            # should be most matched, not only order by increasement_id
            "sort": [{"_score": {"order": "desc"}}, {"increasement_id": {"order": "desc", 'unmapped_type': 'long'}}],
            "size": 20
        }
        result = self.client.search(index=self.index, body=body, ignore_unavailable=True)
        return result

    def display(self, response):
        hits = response['hits']['hits']
        table = PrettyTable(['Title', 'Link', 'increasement_id', '_score'])
        for record in hits:
            source = record['_source']
            row = (source['title'], source.get('url', ''), source['increasement_id'], record['_score'])
            table.add_row(row)
        print(table)

    def search(self, keywords):
        response = self.query(keywords)
        self.display(response)


if __name__ == '__main__':
    # ESSearcher().search('python 内存管理')
    ESSearcher(url='http://192.168.3.185:9200').search('python 内存管理')
