from unittest.mock import MagicMock, patch
from django.test import TestCase
from atlas.apps.account.models import User
from atlas.apps.survei.services import SurveiService
from atlas.apps.survei.models import Pertanyaan, Survei
from rest_framework.test import APIRequestFactory
from datetime import datetime

SURVEI_04 = "survei 04"

class TestSurveiModels(TestCase):

    def setUp(self):
        user_data = {
            'first_name': "indra",
            'last_name': 'mahaarta',
            'email': 'i@gmail.com'
        }

        survei_data_1 = {
            'nama': 'survei 01',
            'deskripsi': 'ini adalah survei pertama',
        }
        survei_data_2 = {
            'nama': 'survei 02',
            'deskripsi': 'ini adalah survei kedua',
        }
        survei_data_3 = {
            'nama': 'survei 03',
            'deskripsi': 'ini adalah survei ketiga',
        }

        self.factory = APIRequestFactory()
        user = User.objects.create(**user_data)
        Survei.objects.create(**survei_data_1, creator=user)
        Survei.objects.create(**survei_data_2, creator=user)
        Survei.objects.create(**survei_data_3, creator=user)
        
        survei = Survei.objects.get(nama = "survei 03")
        survei.sudah_dikirim = True
        survei.save()

    def test_valid_service_register_survei(self):
        request = self.factory.post(path="/api/v3/survei/create", data={
            "nama": SURVEI_04,
            "deskripsi": "lorem ipsum keren"
        })

        request.user = User.objects.get(first_name="indra")
        survei_service = SurveiService()
        survei = survei_service.register_suvei(
            request, SURVEI_04, "keren", datetime.now(), False)
        self.assertEqual(survei, Survei.objects.get(nama=SURVEI_04))

    def test_invalid_service_register_survei(self):
        request = self.factory.post(path="/api/v3/survei/create", data={
            "nama": "Survei 03",
            "deskripsi": "lorem ipsum keren"
        })

        request.user = User.objects.get(first_name="indra")
        User.objects.filter(first_name="indra").delete()
        survei_service = SurveiService()
        survei = survei_service.register_suvei(
            request, "survei 01", "keren", datetime.now(), False)
        self.assertIsNone(survei)

    def test_valid_service_list_survei(self):
        survei_service = SurveiService()
        length = len(survei_service.list_survei())
        self.assertEqual(length, 3)
        
    @patch('atlas.apps.survei.models.Survei.objects.get')
    def test_get_survei_call_objects_get(self, objects_get_mock):
        survei_service = SurveiService()
        survei_service.get_survei(26)
        objects_get_mock.assert_called_once_with(id=26)

    @patch('atlas.apps.survei.models.Survei.objects.get')
    def test_get_survei_return_survei(self, objects_get_mock):
        survei_service = SurveiService()
        survei_mock = MagicMock(spec=Survei)
        objects_get_mock.configure_mock(return_value=survei_mock)
        survei = survei_service.get_survei(26)
        self.assertEqual(survei, survei_mock)

    def test_get_survei_return_none_when_survei_not_exist(self):
        survei_service = SurveiService()
        survei = survei_service.get_survei(100)
        self.assertEqual(survei, None)

    @patch('atlas.apps.survei.models.Pertanyaan.objects.create')
    def test_register_pertanyaan_skala_linier_call_objects_create_and_return(self, objects_create_mock):
        survei_service = SurveiService()
        survei_mock = MagicMock(spec=Survei)
        create_parameters = {
            'survei': survei_mock,
            'pertanyaan': "Apa ya?",
            'wajib_diisi': True
        }
        pertanyaan = survei_service.register_pertanyaan_skala_linier(
            **create_parameters)
        objects_create_mock.assert_called_once_with(
            **create_parameters, jenis_jawaban='Skala Linear')
        self.assertEqual(pertanyaan, objects_create_mock.return_value)

    @patch('atlas.apps.survei.models.OpsiJawaban.objects.create')
    def test_register_opsi_jawaban_skala_linier_call_objects_create_and_return(self, objects_create_mock):
        survei_service = SurveiService()
        pertanyaan_mock = MagicMock(spec=Pertanyaan)
        opsi_jawaban = survei_service.register_opsi_jawaban_skala_linier(
            pertanyaan=pertanyaan_mock, skala=5)
        objects_create_mock.assert_called_once_with(
            pertanyaan=pertanyaan_mock, opsi_jawaban=5)
        self.assertEqual(opsi_jawaban, objects_create_mock.return_value)

    def test_service_list_return_none(self):
        survei_service = SurveiService()
        Survei.objects.filter(nama="survei 01").delete()
        Survei.objects.filter(nama="survei 02").delete()
        Survei.objects.filter(nama="survei 03").delete()
        length = len(survei_service.list_survei())
        self.assertEqual(length, 0)
    
    def test_service_list_sent(self):
        survei_service = SurveiService()
        length = len(survei_service.list_survei_sent())
        self.assertEqual(length, 1)
    
    def test_service_list_not_sent(self):
        survei_service = SurveiService()
        length = len(survei_service.list_survei_not_sent())
        self.assertEqual(length, 2)
