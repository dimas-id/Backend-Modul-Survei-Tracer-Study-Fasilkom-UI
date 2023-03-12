from django.test import TestCase
from atlas.apps.account.models import User
from atlas.apps.survei.models import Survei, Pertanyaan, OpsiJawaban


class TestSurveiModels(TestCase):

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

        opsi_jawaban_data = {
            "opsi_jawaban": "4"
        }

        user = User.objects.create(**user_data)
        survei = Survei.objects.create(
            **survei_data, creator=user)
        pertanyaan = Pertanyaan.objects.create(
            **pertanyaan_data, survei=survei)
        OpsiJawaban.objects.create(
            **opsi_jawaban_data, pertanyaan=pertanyaan)

    def test_valid_model_survei_str(self):
        self.assertEqual(str(Survei.objects.get(
            nama="survei 01")), "survei 01")

    def test_valid_model_pertanyaan_str(self):
        self.assertEqual(str(Pertanyaan.objects.get(
            pertanyaan="1 + 1 = ?")), "survei 01 - 1 + 1 = ?")

    def test_valid_model_opsi_jawabanstr(self):
        self.assertEqual(str(OpsiJawaban.objects.get(
            opsi_jawaban="4")),
            "survei 01 - 1 + 1 = ? - 4")
        print(str(OpsiJawaban.objects.get(opsi_jawaban="4")))
