from rest_framework import status
from atlas.libs.test import RestTestCase
from atlas.apps.account.models import User
from atlas.apps.survei.models import Pertanyaan, Survei


class IsiSurveiTestCase(RestTestCase):
    ISI_SURVEI_URL = '/api/v3/survei/isi'
    JAWABAN_PERTANYAAN_1 = 'jawaban pertanyaan 1'

    def setUp(self):
        user_data = {
            'username':'testuser',
            'email':'test@gmail.com'
        }
        self.user = User.objects.create(**user_data)
        self.survei = Survei.objects.create(
            nama='Test Survei',
            deskripsi='lorem ipsum keren',
            creator=self.user
        )
        self.pertanyaan1 = Pertanyaan.objects.create(
            survei=self.survei,
            pertanyaan='Test Pertanyaan 1',
            wajib_diisi=True
        )
        self.pertanyaan2 = Pertanyaan.objects.create(
            survei=self.survei,
            pertanyaan='Test Pertanyaan 2',
            wajib_diisi=True
        )
        self.authenticate(self.user)

    def test_isi_survei_success(self):

        jawaban = {
            str(self.pertanyaan1.id): self.JAWABAN_PERTANYAAN_1,
            str(self.pertanyaan2.id): 'jawaban pertanyaan 2',
        }
        data = {
            'survei_id': self.survei.id,
            'user_id': self.user.id,
            'jawaban': jawaban
        }
        response = self.client.post(self.ISI_SURVEI_URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_isi_survei_jawaban_is_list_success(self):

        jawaban = {
            str(self.pertanyaan1.id): self.JAWABAN_PERTANYAAN_1,
            str(self.pertanyaan2.id): ['Pilihan_1','Pilihan_2'],
        }
        data = {
            'survei_id': self.survei.id,
            'user_id': self.user.id,
            'jawaban': jawaban
        }
        response = self.client.post(self.ISI_SURVEI_URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_isi_survei_missing_required_answer(self):

        jawaban = {
            str(self.pertanyaan1.id): self.JAWABAN_PERTANYAAN_1,
        }
        data = {
            'survei_id': self.survei.id,
            'user_id': self.user.id,
            'jawaban': jawaban
        }
        response = self.client.post(self.ISI_SURVEI_URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'failed')
        self.assertEqual(response.data['messages'], [str(self.pertanyaan2.id)])

    def test_isi_survei_invalid_answer(self):

        jawaban = {
            str(self.pertanyaan1.id): self.JAWABAN_PERTANYAAN_1,
            str(self.pertanyaan2.id): '',
        }
        data = {
            'survei_id': self.survei.id,
            'user_id': self.user.id,
            'jawaban': jawaban
        }
        response = self.client.post(self.ISI_SURVEI_URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'failed')
        self.assertEqual(response.data['messages'], [str(self.pertanyaan2.id)])

    def test_isi_survei_sudah_diisi(self):

        jawaban = {
            str(self.pertanyaan1.id): self.JAWABAN_PERTANYAAN_1,
            str(self.pertanyaan2.id): 'jawaban pertanyaan 2',
        }
        data = {
            'survei_id': self.survei.id,
            'user_id': self.user.id,
            'jawaban': jawaban
        }
        first_response = self.client.post(self.ISI_SURVEI_URL, data, format='json')
        second_response = self.client.post(self.ISI_SURVEI_URL, data, format='json')
        self.assertEqual(first_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(second_response.status_code, status.HTTP_403_FORBIDDEN)
