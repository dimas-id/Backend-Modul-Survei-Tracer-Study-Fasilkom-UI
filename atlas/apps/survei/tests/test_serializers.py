from django.test import TestCase
from atlas.apps.account.models import User
from atlas.apps.survei.models import Survei
from rest_framework.test import APIRequestFactory
from atlas.apps.survei.serializers import SurveiSerialize


class TestSurveiModels(TestCase):

    def setUp(self):
        user_data = {
            'first_name': "indra",
            'last_name': 'mahaarta',
            'email': 'i@gmail.com'
        }

        survei_data = {
            'nama': 'survei 01',
            'deskripsi': 'ini adalah survei pertama',
        }

        self.factory = APIRequestFactory()
        user = User.objects.create(**user_data)
        Survei.objects.create(**survei_data, creator=user)

    def test_valid_serializer_create_survei(self):
        request = self.factory.post(path="/api/v3/survei/create")
        request.user = User.objects.get(first_name="indra")
        request.data = {
            "nama": "Survei 03",
            "deskripsi": "lorem ipsum keren"
        }

        surver_serialize = SurveiSerialize(
            data=request.data, context={'request': request})
        survei = surver_serialize.create(request.data)
        self.assertEqual(survei, Survei.objects.get(nama="Survei 03"))

    def test_invalid_serializer_create_survei(self):
        request = self.factory.post(path="/api/v3/survei/create")
        request.user = User.objects.get(first_name="indra")
        request.data = {
            "nama": "Survei 03"
        }

        surver_serialize = SurveiSerialize(
            data=request.data, context={'request': request})
        survei = surver_serialize.create(request.data)
        self.assertIsNone(survei)

    def test_valid_serializer_update_survei(self):
        request = self.factory.post(path="/api/v3/survei/create")
        request.user = User.objects.get(first_name="indra")
        request.data = {
            "nama": "Survei 03",
            "deskripsi": "lorem ipsum keren"
        }

        surver_serialize = SurveiSerialize(
            Survei.objects.get(nama="survei 01"), data=request.data, context={'request': request})
        survei = surver_serialize.update(Survei.objects.get(nama = "survei 01"), request.data)
        self.assertNotEqual(str(survei), "survei 01")
        self.assertEqual(str(survei), "Survei 03")
