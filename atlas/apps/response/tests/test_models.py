from django.test import TestCase
from atlas.apps.account.models import User
from atlas.apps.survei.models import Survei, Pertanyaan
from atlas.apps.response.models import Response, Jawaban


class TestResponseModels(TestCase):

    def setUp(self) -> None:
        user_data = {
            'first_name': "indra",
            'last_name': 'mahaarta',
            'email': 'i@gmail.com'
        }

        survei_data = {
            'nama': 'survei 01',
            'deskripsi': 'ini adalah survei pertama',
        }

        pertanyaan_data = {
            "pertanyaan": '1 + 1 = ?',
        }

        jawaban_data = {
            "jawaban": '2'
        }

        user = User.objects.create(**user_data)
        self.survei = Survei.objects.create(
            **survei_data, creator=user)
        self.pertanyaan = Pertanyaan.objects.create(
            **pertanyaan_data, survei=self.survei)
        self.response = Response.objects.create(
            user=user, survei=self.survei
        )
        self.jawaban = Jawaban.objects.create(
            **jawaban_data, response=self.response, pertanyaan=self.pertanyaan
        )

    def test_valid_create_response(self):
        self.assertIsInstance(self.response, Response)

    def test_valid_model_response_str(self):
        self.assertEqual(str(Response.objects.get(
            survei=self.survei)), "i@gmail.com - survei 01")

    def test_valid_create_jawaban(self):
        self.assertIsInstance(self.jawaban, Jawaban)

    def test_valid_model_jawaban_str(self):
        self.assertEqual(str(self.jawaban),
                         "i@gmail.com - survei 01 - 1 + 1 = ? - 2")
