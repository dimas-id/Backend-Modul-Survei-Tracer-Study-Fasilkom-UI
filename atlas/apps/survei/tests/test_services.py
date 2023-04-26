from unittest.mock import MagicMock, Mock, patch
from django.test import TestCase
from atlas.apps.account.models import User
from atlas.apps.survei.services import SurveiService
from atlas.apps.survei.models import Pertanyaan, Survei, OpsiJawaban
from rest_framework import status
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
            'id': 1,
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

        pertanyaan_data_1 = {
            'pertanyaan': 'apakah betul?',
            'wajib_diisi': True,
            'survei_id':1 ,
            'jenis_jawaban': 'Jawaban Singkat'
        }
        pertanyaan_data_2 = {
            'id': 2,
            'pertanyaan': 'apakah benar?',
            'wajib_diisi': True,
            'survei_id':1 ,
            'jenis_jawaban': 'Pilihan Ganda'
        }
        
        opsi_jawaban_1 = {
            'opsi_jawaban': 'Tokopedia',
            'pertanyaan_id': 2
        }
        
        opsi_jawaban_2 = {
            'opsi_jawaban': 'Shopee',
            'pertanyaan_id': 2
        }
        
        self.factory = APIRequestFactory()
        user = User.objects.create(**user_data)
        Survei.objects.create(**survei_data_1, creator=user)
        Survei.objects.create(**survei_data_2, creator=user)
        Survei.objects.create(**survei_data_3, creator=user)
        
        Pertanyaan.objects.create(**pertanyaan_data_1)
        Pertanyaan.objects.create(**pertanyaan_data_2)
        
        OpsiJawaban.objects.create(**opsi_jawaban_1)
        OpsiJawaban.objects.create(**opsi_jawaban_2)
        
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

    @patch('atlas.apps.survei.models.Survei.objects')    
    def test_service_delete_survei_valid(self, survei_objects_mock):
        survei_service = SurveiService()
        mock_survei = MagicMock(spec_set=Survei, id=1)
        survei_objects_mock.get.return_value = mock_survei 

        success_value = (SurveiService.DELETE_SUCCESS, (1, {'Survei': 1}))
        mock_survei.delete.return_value = success_value[1]
        actual_value = survei_service.delete_survei(1)

        survei_objects_mock.get.assert_called_once_with(id=1)
        mock_survei.delete.assert_called_once()
        self.assertEqual(actual_value, success_value)

    @patch('atlas.apps.survei.models.Survei.objects')    
    def test_service_delete_survei_not_found(self, survei_objects_mock):
        survei_service = SurveiService()
        mock_survei = MagicMock(spec_set=Survei, id=1)
        survei_objects_mock.get.side_effect = Survei.DoesNotExist
        
        fail_value = (SurveiService.DELETE_NOT_FOUND, None)
        survei_objects_mock.delete.return_value = fail_value[1]
        actual_value = survei_service.delete_survei(2)

        survei_objects_mock.get.assert_called_once_with(id=2)
        mock_survei.delete.assert_not_called()
        self.assertEqual(actual_value, fail_value)
    
    @patch('atlas.apps.survei.models.Survei.objects')    
    def test_service_delete_survei_published(self, survei_objects_mock):
        survei_service = SurveiService()
        mock_survei = MagicMock(spec_set=Survei, id=1, sudah_dikirim=True)
        survei_objects_mock.get.return_value = mock_survei
        
        fail_value = (SurveiService.DELETE_PUBLISHED, None)
        survei_objects_mock.delete.return_value = fail_value[1]
        actual_value = survei_service.delete_survei(1)

        survei_objects_mock.get.assert_called_once_with(id=1)
        mock_survei.delete.assert_not_called()
        self.assertEqual(actual_value, fail_value)

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
            'pertanyaan': "Mock Question",
            'wajib_diisi': True
        }
        pertanyaan = survei_service.register_pertanyaan_skala_linier(
            **create_parameters)
        objects_create_mock.assert_called_once_with(
            **create_parameters, jenis_jawaban='Skala Linear')
        self.assertEqual(pertanyaan, objects_create_mock.return_value)

    @patch('atlas.apps.survei.models.Pertanyaan.objects.create')
    def test_register_pertanyaan_isian_call_objects_create_and_return(self, objects_create_mock):
        survei_service = SurveiService()
        survei_mock = MagicMock(spec=Survei)
        create_parameters = {
            'survei': survei_mock,
            'pertanyaan': "Mock Question",
            'wajib_diisi': True
        }
        pertanyaan = survei_service.register_pertanyaan_isian(
            **create_parameters)
        objects_create_mock.assert_called_once_with(
            **create_parameters, jenis_jawaban='Jawaban Singkat')
        self.assertEqual(pertanyaan, objects_create_mock.return_value)
    
    @patch('atlas.apps.survei.models.Pertanyaan.objects.create')
    def test_register_pertanyaan_dropdown_call_objects_create_and_return(self, objects_create_mock):
        survei_service = SurveiService()
        survei_mock = MagicMock(spec=Survei)
        create_parameters = {
            'survei': survei_mock,
            'pertanyaan': "Mock Question",
            'wajib_diisi': True
        }
        pertanyaan = survei_service.register_pertanyaan_dropdown(
            **create_parameters)
        objects_create_mock.assert_called_once_with(
            **create_parameters, jenis_jawaban='Drop-Down')
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

    @patch('atlas.apps.survei.models.OpsiJawaban.objects.create')
    def test_register_opsi_jawaban_singkat_call_objects_create_and_return(self, objects_create_mock):
        survei_service = SurveiService()
        pertanyaan_mock = MagicMock(spec=Pertanyaan)
        opsi_jawaban = survei_service.register_opsi_jawaban_isian(
            pertanyaan=pertanyaan_mock, isian="Mock Isian")
        objects_create_mock.assert_called_once_with(
            pertanyaan=pertanyaan_mock, opsi_jawaban="Mock Isian")
        self.assertEqual(opsi_jawaban, objects_create_mock.return_value)

    @patch('atlas.apps.survei.models.OpsiJawaban.objects.create')
    def test_register_opsi_jawaban_dropdown_call_objects_create_and_return(self, objects_create_mock):
        survei_service = SurveiService()
        pertanyaan_mock = MagicMock(spec=Pertanyaan)

        options = ["Jakarta", "Bogor", "Depok", "Tangerang", "Bekasi"]

        opsi_jawaban = survei_service.register_opsi_jawaban_dropdown(
            pertanyaan=pertanyaan_mock, pilihan_jawaban=options)
            
        objects_create_mock.assert_called_once_with(
            pertanyaan=pertanyaan_mock, opsi_jawaban=options)

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

    @patch('atlas.apps.survei.models.Pertanyaan.objects.create')
    def test_register_pertanyaan_radiobutton_call_objects_create_and_return(self, objects_create_mock):
        survei_service = SurveiService()
        survei_mock = MagicMock(spec=Survei)
        
        create_parameters = {
            'survei': survei_mock,
            'pertanyaan': "Lulusan angkatan berapa Anda?",
            'required': True
        }
        
        pertanyaan = survei_service.register_pertanyaan_radiobutton(
            survei=create_parameters["survei"],
            pertanyaan=create_parameters["pertanyaan"],
            wajib_diisi=create_parameters["required"])
        
        objects_create_mock.assert_called_once_with(
            survei=create_parameters["survei"],
            pertanyaan=create_parameters["pertanyaan"],
            wajib_diisi=create_parameters["required"], 
            jenis_jawaban='Pilihan Ganda')
            
        self.assertEqual(pertanyaan, objects_create_mock.return_value)

    @patch('atlas.apps.survei.models.OpsiJawaban.objects.create')
    def test_register_opsi_jawaban_radiobutton_call_objects_create_and_return(self, objects_create_mock):
        survei_service = SurveiService()
        pertanyaan_mock = MagicMock(spec=Pertanyaan)
        
        options = ["2018", "2019", "2020", "2021", "2022"]

        opsi_jawaban = survei_service.register_opsi_jawaban_radiobutton(
            pertanyaan=pertanyaan_mock, 
            pilihan_jawaban=options)
        
        objects_create_mock.assert_called_once_with(
            pertanyaan=pertanyaan_mock, 
            opsi_jawaban=options)
        
        self.assertEqual(opsi_jawaban, objects_create_mock.return_value)

    @patch('atlas.apps.survei.models.Pertanyaan.objects.create')
    def test_register_pertanyaan_checkbox_call_objects_create_and_return(self, objects_create_mock):
        survei_service = SurveiService()
        survei_mock = MagicMock(spec=Survei)
        
        create_parameters = {
            'survei': survei_mock,
            'pertanyaan': "Mata kuliah wajib apakah yang menurut anda berguna bagi pekerjaan anda sekarang ini?",
            'required': True
        }
        
        pertanyaan = survei_service.register_pertanyaan_checkbox(
            survei=create_parameters["survei"],
            pertanyaan=create_parameters["pertanyaan"],
            wajib_diisi=create_parameters["required"])
        
        objects_create_mock.assert_called_once_with(
            survei=create_parameters["survei"],
            pertanyaan=create_parameters["pertanyaan"],
            wajib_diisi=create_parameters["required"], 
            jenis_jawaban='Kotak Centang')
            
        self.assertEqual(pertanyaan, objects_create_mock.return_value)

    @patch('atlas.apps.survei.models.OpsiJawaban.objects.create')
    def test_register_opsi_jawaban_checkbox_call_objects_create_and_return(self, objects_create_mock):
        survei_service = SurveiService()
        pertanyaan_mock = MagicMock(spec=Pertanyaan)
        
        options = ["DDP", "PBP", "SDA", "BasDat", "RPL", "PPL"]

        opsi_jawaban = survei_service.register_opsi_jawaban_checkbox(
            pertanyaan=pertanyaan_mock, 
            pilihan_jawaban=options)
        
        objects_create_mock.assert_called_once_with(
            pertanyaan=pertanyaan_mock, 
            opsi_jawaban=options)
        
        self.assertEqual(opsi_jawaban, objects_create_mock.return_value)
    
    
    def test_service_get_list_pertanyaan(self):
        survei_service = SurveiService()
        length = len(survei_service.get_list_pertanyaan_by_survei_id(1))
        self.assertEqual(length, 2)
    
    def test_service_get_list_pertanyaan_survei_not_found(self):
        survei_service = SurveiService()
        length = len(survei_service.get_list_pertanyaan_by_survei_id(2))
        self.assertEqual(length, 0)
    
    def test_service_get_list_opsi_jawaban(self):
        survei_service = SurveiService()
        length = len(survei_service.get_list_opsi_jawaban(1))
        self.assertEqual(length, 2)
    
    def test_service_get_list_opsi_jawaban_survei_not_found(self):
        survei_service = SurveiService()
        length = len(survei_service.get_list_opsi_jawaban(2))
        self.assertEqual(length, 0)