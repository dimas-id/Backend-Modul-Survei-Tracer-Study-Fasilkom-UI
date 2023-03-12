from django.test import TestCase
from atlas.apps.account.models import User
from atlas.apps.survei.services import SurveiService
from atlas.apps.survei.models import Survei
from rest_framework.test import APIRequestFactory
from datetime import datetime


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

    def test_valid_service_register_survei(self):
        request = self.factory.post(path="/api/v3/survei/create", data={
            "nama": "survei 04",
            "deskripsi": "lorem ipsum keren"
        })

        request.user = User.objects.get(first_name="indra")
        survei_service = SurveiService()
        survei = survei_service.register_suvei(
            request, "survei 04", "keren", datetime.now(), False)
        self.assertEqual(survei, Survei.objects.get(nama="survei 04"))

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
