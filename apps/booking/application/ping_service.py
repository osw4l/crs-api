class PingService:

    def __init__(self, database):
        self.database = database

    def ping(self):
        with self.database.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchall()

        return {'message': 'pong'}


class ElasticSearchService:

    def __init__(self, elastic_search):
        self.elastic_search = elastic_search

    def ping(self):
        if not self.elastic_search.ping():
            raise ValueError("Connection failed")
        return {'message': 'pong'}
