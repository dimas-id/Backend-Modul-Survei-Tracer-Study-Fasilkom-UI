import logging

from django.conf import settings
from elasticsearch import Elasticsearch

from atlas.libs.client import AbstractClientManager
from atlas.libs.elastic import elastic_to_csui_format


def client_factory():
    return Elasticsearch(settings.ELASTICSEARCH_URL)

class ElasticManager(AbstractClientManager):
    client = client_factory()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls_name = self.__class__.__name__
        self.logger = logging.getLogger(cls_name)

    def get_students_by_name(self, name, fail_silently=False):
        try:
            res = self.get_client().search(index=settings.ELASTICSEARCH_INDEX, body={"query": {"match": {"Nama": name}}})
            return elastic_to_csui_format(res), True
        except Exception as e:
            self.logger.error(str(e))
            if not fail_silently:
                raise e

    def get_student_by_npm(self, npm, fail_silently=False):
        try:
            res = self.get_client().search(index=settings.ELASTICSEARCH_INDEX, body={"query": {"match": {"NPM": npm}}})
            return elastic_to_csui_format(res)[0], True, None
        except Exception as e:
            self.logger.error(str(e))
            if not fail_silently:
                raise e
