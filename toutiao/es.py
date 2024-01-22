from elasticsearch import Elasticsearch


class ES:
    def __init__(self, url='http://localhost:9200', index="mytoutiaofav"):
        self.url = url
        self.index = index
        self.client = Elasticsearch([url])