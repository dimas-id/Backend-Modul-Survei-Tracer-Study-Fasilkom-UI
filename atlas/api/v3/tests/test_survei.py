
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

from atlas.apps.survei.models import Pertanyaan, Survei, OpsiJawaban


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
        self.assertEqual(response.data['messages'], [])

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

    def test_create_survei_with_pertanyaan_checkbox_is_valid(self):
        data = {
            'nama': 'Survei pacil checkbox',
            'deskripsi': 'survei tentang pacil checkbox',
            'pertanyaan': [
                self.pertanyaan_checkbox,
            ]
        }
        response = self.client.post(
            self.CREATE_SURVEI_URL, json.dumps(data), content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_survei_with_pertanyaan_dropdown_is_valid(self):
        data = {
            'nama': 'Survei pacil dropdown',
            'deskripsi': 'survei tentang pacil dropdown',
            'pertanyaan': [
                self.pertanyaan_dropdown,
            ]
        }
        response = self.client.post(
            self.CREATE_SURVEI_URL, json.dumps(data), content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

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
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['messages'], [True, False])

    def test_survei_pertanyaan_return_dict_error(self):
        data = {
            "nama": "Survei 03",
            "deskripsi": "lorem ipsum keren",
            "pertanyaan": ['{"a:"}'],
        }
        response = self.client.post(
            self.CREATE_SURVEI_URL, json.dumps(data), content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['messages'], [False])

    def test_survei_pertanyaan_serializer_not_valid_error(self):
        data = {
            'nama': 'Survei test',
            'deskripsi': 'survei yoi',
            'pertanyaan': [{"required": True}]
        }
        response = self.client.post(
            self.CREATE_SURVEI_URL, json.dumps(data), content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['messages'], [False])

    def test_survei_pertanyaan_not_valid_error(self):
        data = {
            'nama': 'Survei test',
            'deskripsi': 'survei yoi',
            'pertanyaan': 'this should be a list'
        }
        response = self.client.post(
            self.CREATE_SURVEI_URL, json.dumps(data), content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['messages'], [])

class TestRegisterSurveiModels(RestTestCase):

    CREATE_SURVEI_URL = "/api/v3/survei/create"
    JSON_CONTENT_TYPE = "application/json"

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = RestTestCase.create_user()
        self.admin = RestTestCase.create_admin()
        self.URL = "/api/v3/survei/finalize"

        survei_data_1 = {
            'id': 1,
            'nama': 'Test Survei',
            'deskripsi': 'ini adalah survei pertama',
        }
        self.survei = Survei.objects.create(**survei_data_1, creator=self.user)


    def test_valid_and_invalid_api_register_survei(self):
        self.authenticate(self.admin)
        response = self.client.get(f'{self.URL}/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(f'{self.URL}/1')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(f'{self.URL}/0')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_user(self):
        self.authenticate(self.user)
        response = self.client.get(f'{self.URL}/1')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestGetSurveiAPI(RestTestCase):
    LIST_SURVEI_URL = "/api/v3/survei/list"
    SURVEI_BY_ID_1_URL = "/api/v3/survei/?survei_id=1"
    SURVEI_BY_ID_2_URL = "/api/v3/survei/?survei_id=2"

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = RestTestCase.create_admin()
        survei_data_1 = {
            'id': 1,
            'nama': 'Test Survei',
            'deskripsi': 'ini adalah survei pertama',
        }
        pertanyaan_data_1 = {
            'pertanyaan': 'q1',
            'wajib_diisi': True,
            'survei_id':1 ,
            'jenis_jawaban': 'Jawaban Singkat'
        }
        pertanyaan_data_2 = {
            'id': 20,
            'pertanyaan': 'q2',
            'wajib_diisi': True,
            'survei_id':1 ,
            'jenis_jawaban': 'Pilihan Ganda'
        }
        
        opsi_jawaban_1 = {
            'opsi_jawaban': 'Google',
            'pertanyaan_id': 20
        }
        
        opsi_jawaban_2 = {
            'opsi_jawaban': 'Chat GPT',
            'pertanyaan_id': 20
        }
        
        self.survei = Survei.objects.create(**survei_data_1, creator=self.user)
        self.pertanyaan1 = Pertanyaan.objects.create(**pertanyaan_data_1)
        self.pertanyaan2 = Pertanyaan.objects.create(**pertanyaan_data_2)
        self.opsi_jawaban_1 = OpsiJawaban.objects.create(**opsi_jawaban_1)
        self.opsi_jawaban_2 = OpsiJawaban.objects.create(**opsi_jawaban_2)
        

    def test_valid_get_survei(self):
        self.authenticate(self.user)
        response = self.client.get(
            self.LIST_SURVEI_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_survei_not_authorized(self):
        response = self.client.get(
            self.LIST_SURVEI_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_survei_by_id(self):
        self.authenticate(self.user)
        
        response = self.client.get(self.SURVEI_BY_ID_1_URL)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['survei']['nama'], 'Test Survei')
        self.assertEqual(len(response.data['list_pertanyaan']), 2)
        self.assertEqual(len(response.data['list_opsi_jawaban']), 2)
    
    def test_get_survei_by_id_not_found(self):
        self.authenticate(self.user)
        response = self.client.get(
            self.SURVEI_BY_ID_2_URL)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class TestEditSurveiModels(RestTestCase):
    EDIT_SURVEI_URL = "/api/v3/survei/edit"
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

    def test_valid_api_edit_survei(self):
        data = {
            "nama": "Survei 12",
            "deskripsi": "lorem ipsum keren",
            "pertanyaan": [],
        }
        response = self.client.put(
            self.EDIT_SURVEI_URL, json.dumps(data), content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_api_edit_survei(self):
        data = {
            "nama": "Survei 03",
            "deskripsi": "",
        }
        response = self.client.put(
            self.EDIT_SURVEI_URL, json.dumps(data), content_type=self.JSON_CONTENT_TYPE)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['messages'], [])

    def test_edit_survei_with_pertanyaan_skala_linier_is_valid(self):
        data = {
            'nama': 'Survei pacil skala',
            'deskripsi': 'survei tentang pacil skala',
            'pertanyaan': [
                self.pertanyaan_skala_linier,
            ]
        }
        response = self.client.put(
            self.EDIT_SURVEI_URL, json.dumps(data), content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_survei_with_pertanyaan_isian_is_valid(self):
        data = {
            'nama': 'Survei pacil isian',
            'deskripsi': 'survei tentang pacil isian',
            'pertanyaan': [
                self.pertanyaan_isian,
            ]
        }
        response = self.client.put(
            self.EDIT_SURVEI_URL, json.dumps(data), content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_survei_with_pertanyaan_pilihan_ganda_is_valid(self):
        data = {
            'nama': 'Survei pacil ganda',
            'deskripsi': 'survei tentang pacil ganda',
            'pertanyaan': [
                self.pertanyaan_pilihan_ganda,
            ]
        }
        response = self.client.put(
            self.EDIT_SURVEI_URL, json.dumps(data), content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_survei_with_pertanyaan_checkbox_is_valid(self):
        data = {
            'nama': 'Survei pacil checkbox',
            'deskripsi': 'survei tentang pacil checkbox',
            'pertanyaan': [
                self.pertanyaan_checkbox,
            ]
        }
        response = self.client.put(
            self.EDIT_SURVEI_URL, json.dumps(data), content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_survei_with_pertanyaan_dropdown_is_valid(self):
        data = {
            'nama': 'Survei pacil dropdown',
            'deskripsi': 'survei tentang pacil dropdown',
            'pertanyaan': [
                self.pertanyaan_dropdown,
            ]
        }
        response = self.client.put(
            self.EDIT_SURVEI_URL, json.dumps(data), content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_survei_not_valid_pertanyaan(self):
        data = {
            'nama': 'Survei pacil',
            'deskripsi': 'survei tentang pacil',
            'pertanyaan': [
                self.pertanyaan_skala_linier,
                {"apa ini": "apa ini"},
            ]
        }
        response = self.client.put(
            self.EDIT_SURVEI_URL, json.dumps(data), content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['messages'], [True, False])

    def test_survei_pertanyaan_return_dict_error(self):
        data = {
            "nama": "Survei 03",
            "deskripsi": "lorem ipsum keren",
            "pertanyaan": ['{"a:"}'],
        }
        response = self.client.put(
            self.EDIT_SURVEI_URL, json.dumps(data), content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['messages'], [False])

    def test_survei_pertanyaan_serializer_not_valid_error(self):
        data = {
            'nama': 'Survei test',
            'deskripsi': 'survei yoi',
            'pertanyaan': [{"required": True}]
        }
        response = self.client.put(
            self.EDIT_SURVEI_URL, json.dumps(data), content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['messages'], [False])

    def test_survei_pertanyaan_not_valid_error(self):
        data = {
            'nama': 'Survei test',
            'deskripsi': 'survei yoi',
            'pertanyaan': 'this should be a list'
        }
        response = self.client.put(
            self.EDIT_SURVEI_URL, json.dumps(data), content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['messages'], [])

class TestDeleteSurveiAPI(RestTestCase):
    ID_VALID = 1
    ID_PUBLISHED = 2
    ID_NOT_EXIST = 3
    ENDPOINT = "/api/v3/survei/delete/?survei_id="

    def setUp(self):
        self.factory = APIRequestFactory()
        self.admin_user = RestTestCase.create_admin()
        self.non_admin_user = RestTestCase.create_user()
        survei_data_1 = {
            'id': self.ID_VALID,
            'nama': 'Test Survei',
            'deskripsi': 'ini adalah survei pertama',
            'sudah_dikirim': False
        }
        survei_data_2 = {
            'id': self.ID_PUBLISHED,
            'nama': 'Test Survei',
            'deskripsi': 'ini adalah survei kedua. Survei ini sudah dikirim.',
            'sudah_dikirim': True
        }
        self.survei = Survei.objects.create(**survei_data_1, creator=self.admin_user)
        self.pertanyaan1 = Survei.objects.create(**survei_data_2, creator=self.admin_user)
        
    def test_delete_survei_by_id(self):
        self.authenticate(self.admin_user)
        response = self.client.delete(self.ENDPOINT + str(self.ID_VALID))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)

    def test_delete_survei_by_id_not_authorized(self):
        response = self.client.delete(self.ENDPOINT + str(self.ID_VALID))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_delete_survei_by_id_not_admin(self):
        self.authenticate(self.non_admin_user)
        response = self.client.delete(self.ENDPOINT + str(self.ID_VALID))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_survei_by_id_not_exist(self):
        self.authenticate(self.admin_user)
        response = self.client.delete(self.ENDPOINT + str(self.ID_NOT_EXIST))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_survei_by_id_published(self):
        self.authenticate(self.admin_user)
        response = self.client.delete(self.ENDPOINT + str(self.ID_PUBLISHED))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
