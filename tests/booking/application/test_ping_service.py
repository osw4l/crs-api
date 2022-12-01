from django.db import connection
from django.test import TestCase
from elasticsearch import Elasticsearch
from django.conf import settings

from apps.booking.application.ping_service import PingService, ElasticSearchService


class PingServiceTest(TestCase):

    def setUp(self):
        self.ping_service = PingService(connection)

    def test_get_ping(self):
        response = self.ping_service.ping()
        self.assertEqual(response, {'message': 'pong'})


class PingElasticSearch(TestCase):
    def setUp(self):
        elastic_host = settings.ELASTICSEARCH_DSL.get('default').get('hosts')
        elastic_search = Elasticsearch([f'http://{elastic_host}/'], verify_certs=True)
        self.ping_service = ElasticSearchService(elastic_search=elastic_search)

    def test_get_ping(self):
        response = self.ping_service.ping()
        self.assertEqual(response, {'message': 'pong'})
