from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Rate


@registry.register_document
class RateDocument(Document):
    """
    RateDocument: Elasticsearch document to avoid to hit the database
    """
    room = fields.ObjectField(properties={
        'code': fields.TextField(),
    })

    class Index:
        name = 'rates'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Rate
        fields = [
            'name',
            'code'
        ]

