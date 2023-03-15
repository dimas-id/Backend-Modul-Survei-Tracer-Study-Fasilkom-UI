from unittest.mock import MagicMock
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
        self.survei = Survei.objects.create(
            **survei_data, creator=user)
        self.pertanyaan = Pertanyaan.objects.create(
            **pertanyaan_data, survei=self.survei)
        self.opsi_jawaban = OpsiJawaban.objects.create(
            **opsi_jawaban_data, pertanyaan=self.pertanyaan)

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

    def test_create_pertanyaan_is_valid(self):
        pertanyaan = Pertanyaan.objects.create(
            survei=self.survei,
            pertanyaan="15 * 1 = ?",
            jenis_jawaban='Pilihan Ganda',
            wajib_diisi=True
        )

        self.assertIsInstance(pertanyaan, Pertanyaan)

    def test_create_opsi_jawaban_is_valid(self):
        opsi_jawaban = OpsiJawaban.objects.create(
            pertanyaan=self.pertanyaan,
            opsi_jawaban="15",
        )

        self.assertIsInstance(opsi_jawaban, OpsiJawaban)
