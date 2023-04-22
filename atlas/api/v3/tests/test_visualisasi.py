from rest_framework import status
from atlas.libs.test import RestTestCase
from atlas.apps.survei.models import Pertanyaan, Survei, OpsiJawaban
from atlas.apps.response.models import Response, Jawaban
from rest_framework.test import APIRequestFactory
from rest_framework import status


class VisualisasiTest(RestTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = RestTestCase.create_admin()
        self.common_user = RestTestCase.create_user()

        self.survei = Survei.objects.create(
            nama='Test Visualisasi Survei',
            deskripsi='Ini adalah Survei untuk keperluhan test visualisasi',
            creator=self.user
        )
        self.pertanyaan1 = Pertanyaan.objects.create(
            survei=self.survei,
            pertanyaan='1 + 1 = ?',
            jenis_jawaban="Jawaban Singkat",
            wajib_diisi=True
        )
        self.pertanyaan2 = Pertanyaan.objects.create(
            survei=self.survei,
            pertanyaan='0 + 2 = ?',
            jenis_jawaban="Skala Linear",
            wajib_diisi=True
        )
        self.opsi_jawaban21 = OpsiJawaban.objects.create(
            pertanyaan=self.pertanyaan2,
            opsi_jawaban="0"
        )
        self.opsi_jawaban22 = OpsiJawaban.objects.create(
            pertanyaan=self.pertanyaan2,
            opsi_jawaban="1"
        )
        self.opsi_jawaban23 = OpsiJawaban.objects.create(
            pertanyaan=self.pertanyaan2,
            opsi_jawaban="2"
        )
        self.pertanyaan3 = Pertanyaan.objects.create(
            survei=self.survei,
            pertanyaan='1 + 3 = ?',
            jenis_jawaban="Pilihan Ganda",
            wajib_diisi=True
        )
        self.opsi_jawaban32 = OpsiJawaban.objects.create(
            pertanyaan=self.pertanyaan2,
            opsi_jawaban="4"
        )
        self.opsi_jawaban32 = OpsiJawaban.objects.create(
            pertanyaan=self.pertanyaan2,
            opsi_jawaban="5"
        )
        self.opsi_jawaban33 = OpsiJawaban.objects.create(
            pertanyaan=self.pertanyaan3,
            opsi_jawaban="6"
        )
        self.pertanyaan4 = Pertanyaan.objects.create(
            survei=self.survei,
            pertanyaan='1 + 4 = ?',
            jenis_jawaban="Drop-Down",
            wajib_diisi=True
        )
        self.opsi_jawaban41 = OpsiJawaban.objects.create(
            pertanyaan=self.pertanyaan4,
            opsi_jawaban="4"
        )
        self.opsi_jawaban42 = OpsiJawaban.objects.create(
            pertanyaan=self.pertanyaan4,
            opsi_jawaban="5"
        )
        self.opsi_jawaban43 = OpsiJawaban.objects.create(
            pertanyaan=self.pertanyaan4,
            opsi_jawaban="6"
        )
        self.pertanyaan5 = Pertanyaan.objects.create(
            survei=self.survei,
            pertanyaan='1 + 5 = ?',
            jenis_jawaban="Kotak Centang",
            wajib_diisi=True
        )
        self.opsi_jawaban51 = OpsiJawaban.objects.create(
            pertanyaan=self.pertanyaan5,
            opsi_jawaban="4"
        )
        self.opsi_jawaban52 = OpsiJawaban.objects.create(
            pertanyaan=self.pertanyaan5,
            opsi_jawaban="5"
        )
        self.opsi_jawaban52 = OpsiJawaban.objects.create(
            pertanyaan=self.pertanyaan5,
            opsi_jawaban="6"
        )

        self.response = Response.objects.create(
            survei=self.survei,
            user=self.user
        )

        self.jawaban1 = Jawaban.objects.create(
            pertanyaan=self.pertanyaan1,
            response=self.response,
            jawaban="2"
        )

        self.jawaban2 = Jawaban.objects.create(
            pertanyaan=self.pertanyaan2,
            response=self.response,
            jawaban="2"
        )

        self.jawaban3 = Jawaban.objects.create(
            pertanyaan=self.pertanyaan3,
            response=self.response,
            jawaban="4"
        )

        self.jawaban4 = Jawaban.objects.create(
            pertanyaan=self.pertanyaan4,
            response=self.response,
            jawaban="5"
        )

        self.jawaban5 = Jawaban.objects.create(
            pertanyaan=self.pertanyaan5,
            response=self.response,
            jawaban="6"
        )

    def test_get_invalid_non_admin_user(self):
        self.authenticate(self.common_user)

        s = Survei.objects.get(nama="Test Visualisasi Survei")
        response = self.client.get(f"/api/v3/visualisasi/{s.id}")
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_survei_id(self):
        self.authenticate(self.user)

        response = self.client.get("/api/v3/visualisasi/676")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_valid_visualisasi(self):
        self.authenticate(self.user)

        s = Survei.objects.get(nama="Test Visualisasi Survei")
        response = self.client.get(f"/api/v3/visualisasi/{s.id}")
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['survei']["nama"], "Test Visualisasi Survei")
        self.assertEqual(data['responden'], 1)
        self.assertEqual(len(data['pertayaan']), 5)
