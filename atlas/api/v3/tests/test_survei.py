
import json
from unittest.mock import Mock, patch
from atlas.api.v3.views.survei import register_survei
from atlas.apps.account.models import User
from rest_framework.test import APIRequestFactory, APITestCase
from django.urls import reverse
from rest_framework import status
from django.urls import reverse

from atlas.apps.survei.serializers import RadioButtonRequestSerializer
from atlas.libs.test import RestTestCase


class TestRegisterSurveiModels(RestTestCase):

    CREATE_SURVEI_URL = "/api/v3/survei/create"
    JSON_CONTENT_TYPE = "application/json"

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = RestTestCase.create_admin()
        self.authenticate(self.user)

        self.pertanyaan_pilihan_ganda = {
            "pertanyaan": "Pertanyaan Pilihan ganda",
            "required": True,
            "tipe": "Pilihan Ganda",
            "option": {
                "data": ["1", "2", "3"]
            }
        }

        self.pertanyaan_skala_linier = {
            "pertanyaan": "1 sampai 7",
            "required": True,
            "tipe": "Skala Linear",
            "option": {
                    "banyak_skala": 7,
            }
        }

        self.pertanyaan_isian = {
            "pertanyaan": "1 sampai 7",
            "required": True,
            "tipe": "Jawaban Singkat",
        }

        self.pertanyaan_checkbox = {
            "pertanyaan": "Pertanyaan CheckBox",
            "required": True,
            "tipe": "Kotak Centang",
            "option": {
                "data": ["1", "2", "3"]
            }
        }

        self.pertanyaan_dropdown = {
            "pertanyaan": "Pertanyaan CheckBox",
            "required": True,
            "tipe": "Drop-Down",
            "option": {
                "data": ["1", "2", "3"]
            }
        }

    def test_valid_api_register_survei(self):
        data = {
            "nama": "Survei 12",
            "deskripsi": "lorem ipsum keren",
            "pertanyaan": [],
        }
        response = self.client.post(
            self.CREATE_SURVEI_URL, json.dumps(data), content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_api_register_survei(self):
        data = {
            "nama": "Survei 03"
        }
        response = self.client.post(
            self.CREATE_SURVEI_URL, json.dumps(data), content_type=self.JSON_CONTENT_TYPE)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_survei_with_pertanyaan_skala_linier_is_valid(self):
        data = {
            'nama': 'Survei pacil skala',
            'deskripsi': 'survei tentang pacil skala',
            'pertanyaan': [
                self.pertanyaan_skala_linier,
            ]
        }
        response = self.client.post(
            self.CREATE_SURVEI_URL, json.dumps(data), content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['errors']), 0)

    def test_create_survei_with_pertanyaan_isian_is_valid(self):
        data = {
            'nama': 'Survei pacil isian',
            'deskripsi': 'survei tentang pacil isian',
            'pertanyaan': [
                self.pertanyaan_isian,
            ]
        }
        response = self.client.post(
            self.CREATE_SURVEI_URL, json.dumps(data), content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['errors']), 0)

    def test_create_survei_with_pertanyaan_pilihan_ganda_is_valid(self):
        data = {
            'nama': 'Survei pacil ganda',
            'deskripsi': 'survei tentang pacil ganda',
            'pertanyaan': [
                self.pertanyaan_pilihan_ganda,
            ]
        }
        response = self.client.post(
            self.CREATE_SURVEI_URL, json.dumps(data), content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['errors']), 0)

    def test_create_survei_with_pertanyaan_checkbox_is_valid(self):
        data = {
            'nama': 'Survei pacil ganda',
            'deskripsi': 'survei tentang pacil ganda',
            'pertanyaan': [
                self.pertanyaan_checkbox,
            ]
        }
        response = self.client.post(
            self.CREATE_SURVEI_URL, json.dumps(data), content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['errors']), 0)

    def test_create_survei_with_pertanyaan_dropdown_is_valid(self):
        data = {
            'nama': 'Survei pacil ganda',
            'deskripsi': 'survei tentang pacil ganda',
            'pertanyaan': [
                self.pertanyaan_dropdown,
            ]
        }
        response = self.client.post(
            self.CREATE_SURVEI_URL, json.dumps(data), content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['errors']), 0)

    def test_create_survei_not_valid_pertanyaan(self):
        data = {
            'nama': 'Survei pacil',
            'deskripsi': 'survei tentang pacil',
            'pertanyaan': [
                self.pertanyaan_skala_linier,
                {"apa ini": "apa ini"},
            ]
        }
        response = self.client.post(
            self.CREATE_SURVEI_URL, json.dumps(data), content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['errors']), 1)

    def test_survei_pertanyaan_return_dict_error(self):
        data = {
            "nama": "Survei 03",
            "deskripsi": "lorem ipsum keren",
            "pertanyaan": ['{"a:"}'],
        }
        response = self.client.post(
            self.CREATE_SURVEI_URL, json.dumps(data), content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(len(response.data['errors']), 1)

    def test_survei_pertanyaan_serializer_not_valid_error(self):
        data = {
            'nama': 'Survei test',
            'deskripsi': 'survei yoi',
            'pertanyaan': [{"required": True}]
        }
        response = self.client.post(
            self.CREATE_SURVEI_URL, json.dumps(data), content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(len(response.data['errors']), 1)


class TestGetSurveiAPI(RestTestCase):
    LIST_SURVEI_URL = "/api/v3/survei/list"

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = RestTestCase.create_admin()

    def test_valid_get_survei(self):
        self.authenticate(self.user)
        response = self.client.get(
            self.LIST_SURVEI_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_survei_not_authorized(self):
        response = self.client.get(
            self.LIST_SURVEI_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)