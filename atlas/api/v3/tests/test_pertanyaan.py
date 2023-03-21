from unittest.mock import patch
from rest_framework.test import APIRequestFactory
from rest_framework import status

from atlas.libs.test import RestTestCase


class TestSkalaLiner(RestTestCase):

    CREATE_SKALA_LINER = "/api/v3/pertanyaan/create/skala-linier"

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = RestTestCase.create_admin()

    def test_register_skala_liner_not_authenticated(self):
        request = self.factory.post(path=self.CREATE_SKALA_LINER)
        response = self.client.post(
            self.CREATE_SKALA_LINER, request=request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('atlas.api.v3.views.pertanyaan.SkalaLinierRequestSerializer')
    def test_register_skala_liner_call_request_serializer(self, serializer_mock):
        self.authenticate(self.user)
        request = self.factory.post(path=self.CREATE_SKALA_LINER)
        self.client.post(
            self.CREATE_SKALA_LINER, request=request)
        serializer_mock.assert_called_once()

    @patch('atlas.api.v3.views.pertanyaan.SkalaLinierRequestSerializer')
    def test_register_return_400_when_serializer_is_not_valid(self, skala_linier_mock):
        self.authenticate(self.user)
        skala_linier_mock.return_value.is_valid.return_value = False
        request = self.factory.post(path=self.CREATE_SKALA_LINER)
        response = self.client.post(
            self.CREATE_SKALA_LINER, request=request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('atlas.api.v3.views.pertanyaan.SkalaLinierRequestSerializer')
    def test_register_return_201_when_serializer_is_valid(self, skala_linier_mock):
        self.authenticate(self.user)
        skala_linier_mock.return_value.is_valid.return_value = True
        request = self.factory.post(path=self.CREATE_SKALA_LINER)
        response = self.client.post(
            self.CREATE_SKALA_LINER, request=request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class TestIsian(RestTestCase):

    CREATE_ISIAN = "/api/v3/pertanyaan/create/jawaban-singkat"

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = RestTestCase.create_admin()

    def test_register_isian_not_authenticated(self):
        request = self.factory.post(path=self.CREATE_ISIAN)
        response = self.client.post(
            self.CREATE_ISIAN, request=request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('atlas.api.v3.views.pertanyaan.IsianRequestSerializer')
    def test_register_isian_call_request_serializer(self, serializer_mock):
        self.authenticate(self.user)
        request = self.factory.post(path=self.CREATE_ISIAN)
        self.client.post(
            self.CREATE_ISIAN, request=request)
        serializer_mock.assert_called_once()

    @patch('atlas.api.v3.views.pertanyaan.IsianRequestSerializer')
    def test_register_return_400_when_serializer_is_not_valid(self, isian_mock):
        self.authenticate(self.user)
        isian_mock.return_value.is_valid.return_value = False
        request = self.factory.post(path=self.CREATE_ISIAN)
        response = self.client.post(
            self.CREATE_ISIAN, request=request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('atlas.api.v3.views.pertanyaan.IsianRequestSerializer')
    def test_register_return_201_when_serializer_is_valid(self, isian_mock):
        self.authenticate(self.user)
        isian_mock.return_value.is_valid.return_value = True
        request = self.factory.post(path=self.CREATE_ISIAN)
        response = self.client.post(
            self.CREATE_ISIAN, request=request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
