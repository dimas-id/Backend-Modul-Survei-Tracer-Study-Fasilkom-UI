from django.test import TestCase
from django.db import transaction
from atlas.apps.response.models import Response, Jawaban
from atlas.apps.survei.models import Survei, Pertanyaan
from atlas.apps.account.models import User
from atlas.apps.response.services import ResponseService
from unittest.mock import MagicMock, Mock, patch

class ResponseServiceTestCase(TestCase):
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
            jenis_jawaban = 'Jawaban Singkat',
            wajib_diisi=True
        )
        self.pertanyaan2 = Pertanyaan.objects.create(
            survei=self.survei,
            pertanyaan='Test Pertanyaan 2',
            jenis_jawaban = 'Jawaban Singkat',
            wajib_diisi=True
        )
        self.response_service = ResponseService()

    @transaction.atomic
    def test_register_response(self):
        response = self.response_service.register_response(
            user_id=self.user.id,
            survei=self.survei
        )

        self.assertIsInstance(response, Response)
        self.assertEqual(response.user, self.user)
        self.assertEqual(response.survei, self.survei)

    @transaction.atomic
    @patch('atlas.apps.response.models.Response.objects')
    def test_get_response_success(self, response_objects_mock):
        mock_response = MagicMock(spec_set=Response, user_id=self.user.id, survei=self.survei)
        response_objects_mock.get.return_value = mock_response

        success_value = mock_response
        actual_value = self.response_service.get_response(self.user.id, self.survei.id)

        response_objects_mock.get.assert_called_once_with(user_id=self.user.id, survei_id=self.survei.id)

        self.assertEqual(success_value, actual_value)

    @transaction.atomic
    @patch('atlas.apps.response.models.Response.objects')
    def test_get_response_not_found(self, response_objects_mock):
        response_objects_mock.get.side_effect = Response.DoesNotExist

        fail_value = None
        actual_value = self.response_service.get_response(self.user.id, self.survei.id)

        response_objects_mock.get.assert_called_once_with(user_id=self.user.id, survei_id=self.survei.id)

        self.assertEqual(fail_value, actual_value)

    @transaction.atomic
    def test_register_jawaban(self):
        response = self.response_service.register_response(
            user_id=self.user.id,
            survei=self.survei
        )
        jawaban1 = 'Jawaban 1'
        jawaban2 = 'Jawaban 2'
        new_jawaban1 = self.response_service.register_jawaban(
            pertanyaan=self.pertanyaan1,
            response=response,
            jawaban=jawaban1
        )
        new_jawaban2 = self.response_service.register_jawaban(
            pertanyaan=self.pertanyaan1,
            response=response,
            jawaban=jawaban2
        )

        self.assertIsInstance(new_jawaban1, Jawaban)
        self.assertIsInstance(new_jawaban2, Jawaban)
        self.assertEqual(new_jawaban1.response, response)
        self.assertEqual(new_jawaban2.response, response)
        self.assertEqual(new_jawaban1.pertanyaan, self.pertanyaan1)
        self.assertEqual(new_jawaban2.pertanyaan, self.pertanyaan1)
        self.assertEqual(new_jawaban1.jawaban, jawaban1)
        self.assertEqual(new_jawaban2.jawaban, jawaban2)

    def test_valid_jawaban(self):
        pertanyaan_id_list = [1, 2, 3]
        jawaban_keys_list = ['1', '2', '3']
        jawaban = {'1': 'jawaban1', '2': ['jawaban2'], '3': 'jawaban3'}
        
        result = self.response_service.check_jawaban_validity(pertanyaan_id_list, jawaban_keys_list, jawaban)
        
        self.assertEqual(len(result), 0)
    
    def test_invalid_jawaban(self):
        pertanyaan_id_list = [1, 2, 3]
        jawaban_keys_list = ['1', '2']
        jawaban = {'1': 'jawaban1', '2': []}
        
        result = self.response_service.check_jawaban_validity(pertanyaan_id_list, jawaban_keys_list, jawaban)
        
        self.assertEqual(len(result), 2)
        self.assertIn('2', result)
        self.assertIn('3', result)