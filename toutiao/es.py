from elasticsearch import Elasticsearch


class ES:
    def __init__(self, url='http://localhost:9200', index="mytoutiaofav"):
        self.url = url
        self.index = index
        self.client = Elasticsearch([url],timeout=60, max_retries=10, retry_on_timeout=True)