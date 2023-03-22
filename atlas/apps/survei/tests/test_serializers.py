from unittest.mock import MagicMock, Mock, call, patch
from django.test import TestCase
from atlas.apps.account.models import User
from atlas.apps.survei.models import OpsiJawaban, Pertanyaan, Survei
from rest_framework.test import APIRequestFactory
from atlas.apps.survei.serializers import OpsiJawabanSerializer, PertanyaanSerializer, SkalaLinierRequestSerializer, IsianRequestSerializer, SurveiSerialize, RadioButtonRequestSerializer
from rest_framework import serializers

SURVEI_01 = "survei 01"
SURVEI_03 = "Survei 03"
API_SURVEI_CREATE = "/api/v3/survei/create"

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
        request = self.factory.post(path=API_SURVEI_CREATE)
        request.user = User.objects.get(first_name="indra")
        request.data = {
            "nama": SURVEI_03,
            "deskripsi": "lorem ipsum keren"
        }

        surver_serialize = SurveiSerialize(
            data=request.data, context={'request': request})
        survei = surver_serialize.create(request.data)
        self.assertEqual(survei, Survei.objects.get(nama=SURVEI_03))

    def test_invalid_serializer_create_survei(self):
        request = self.factory.post(path=API_SURVEI_CREATE)
        request.user = User.objects.get(first_name="indra")
        request.data = {
            "nama": SURVEI_03
        }

        surver_serialize = SurveiSerialize(
            data=request.data, context={'request': request})
        survei = surver_serialize.create(request.data)
        self.assertIsNone(survei)

    def test_valid_serializer_update_survei(self):
        request = self.factory.post(path=API_SURVEI_CREATE)
        request.user = User.objects.get(first_name="indra")
        request.data = {
            "nama": SURVEI_03,
            "deskripsi": "lorem ipsum keren"
        }

        surver_serialize = SurveiSerialize(
            Survei.objects.get(nama="survei 01"), data=request.data, context={'request': request})
        survei = surver_serialize.update(Survei.objects.get(nama = "survei 01"), request.data)
        self.assertNotEqual(str(survei), "survei 01")
        self.assertEqual(str(survei), "Survei 03")

class TestPertanyaanSerializer(TestCase):

    def setUp(self):

        self.pertanyaan_data = {
            'id': 1,
            'pertanyaan': 'Ini pertanyaan?',
            'jenis_jawaban': 'Drop-Down',
            'wajib_diisi': True,
        }

        self.serializer = PertanyaanSerializer(
            data=self.pertanyaan_data)

    def test_contains_expected_fields(self):
        fields = self.serializer.get_fields()
        self.assertEqual(set(fields), set(
            ['id', 'pertanyaan', 'jenis_jawaban', 'wajib_diisi']))


class TestOpsiJawabanSerializer(TestCase):

    def setUp(self):

        self.opsi_jawaban_data = {
            'id': 1,
            'opsi_jawaban': 'Opsi 1',
        }

        self.serializer = OpsiJawabanSerializer(
            data=self.opsi_jawaban_data)

    def test_contains_expected_fields(self):
        fields = self.serializer.get_fields()
        self.assertEqual(set(fields), set(
            ['id', 'opsi_jawaban']))


class TestSkalaLinierRequestSerializer(TestCase):

    def setUp(self) -> None:
        self.serializer_data = {
            'survei_id': 1,
            'pertanyaan': 'Dari 1-5 seberapa puas anda?',
            'pertanyaan_wajib_diisi': True,
            'banyak_skala': 5,
            'mulai_dari_satu': True,
        }

        self.serializer = SkalaLinierRequestSerializer(
            data=self.serializer_data)

    def test_request_contains_expected_fields(self):
        fields = self.serializer.get_fields()
        self.assertEqual(set(fields), set(
            ['survei_id', 'pertanyaan', 'pertanyaan_wajib_diisi', 'banyak_skala', 'mulai_dari_satu']))

    @patch('atlas.apps.survei.services.SurveiService.get_survei')
    def test_initial_request_is_valid(self, get_survei_mock):
        self.assertTrue(self.serializer.is_valid())

    @patch('atlas.apps.survei.services.SurveiService.get_survei')
    def test_survei_id_is_required(self, get_survei_mock):
        self.serializer_data.pop('survei_id')
        serializer = SkalaLinierRequestSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())

    @patch('atlas.apps.survei.services.SurveiService.get_survei')
    def test_pertanyaan_is_required(self, get_survei_mock):
        self.serializer_data.pop('pertanyaan')
        serializer = SkalaLinierRequestSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())

    @patch('atlas.apps.survei.services.SurveiService.get_survei')
    def test_banyak_skala_is_min_2(self, get_survei_mock):
        self.serializer_data['banyak_skala'] = 1
        serializer = SkalaLinierRequestSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())

        self.serializer_data['banyak_skala'] = 2
        serializer = SkalaLinierRequestSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())

    @patch('atlas.apps.survei.services.SurveiService.get_survei')
    def test_banyak_skala_is_max_15(self, get_survei_mock):
        self.serializer_data['banyak_skala'] = 15
        serializer = SkalaLinierRequestSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())

        self.serializer_data['banyak_skala'] = 16
        serializer = SkalaLinierRequestSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())

    @patch('atlas.apps.survei.services.SurveiService.get_survei')
    def test_validate_called_get_survei_once(self, get_survei_mock):
        self.serializer.is_valid()
        get_survei_mock.assert_called_once()

    @patch('atlas.apps.survei.services.SurveiService.get_survei', Mock(return_value=None))
    def test_validate_should_fail_if_get_survei_return_none(self):
        self.assertFalse(self.serializer.is_valid())

    @patch('atlas.apps.survei.services.SurveiService.get_survei', Mock(return_value=None))
    def test_validate_should_raise_error_if_get_survei_return_none(self):
        self.serializer.is_valid()
        self.assertRaises(serializers.ValidationError)

    @patch('atlas.apps.survei.services.SurveiService.get_survei', Mock(return_value=True))
    def test_validate_should_succeed_if_get_survei_return_some(self):
        self.assertTrue(self.serializer.is_valid())

    @patch('atlas.apps.survei.services.SurveiService.get_survei', Mock(return_value=None))
    def test_validate_survey_id_should_raise_with_correct_message(self):
        with self.assertRaises(serializers.ValidationError) as exc:
            self.serializer.validate_survei_id(1)
        self.assertEqual(str(exc.exception.detail[0]),
                         "Survei with id 1 does not exist")

    @patch('atlas.apps.survei.services.SurveiService.register_opsi_jawaban_skala_linier')
    @patch('atlas.apps.survei.services.SurveiService.register_pertanyaan_skala_linier')
    @patch('atlas.apps.survei.services.SurveiService.get_survei')
    def test_create_should_call_get_survei_once_with_param(self, get_survei_mock, register_pertanyaan_mock, register_opsi_jawaban_mock):
        self.serializer.create(self.serializer_data)
        get_survei_mock.assert_called_once_with(
            self.serializer_data['survei_id'])

    @patch('atlas.apps.survei.services.SurveiService.register_opsi_jawaban_skala_linier')
    @patch('atlas.apps.survei.services.SurveiService.register_pertanyaan_skala_linier')
    @patch('atlas.apps.survei.services.SurveiService.get_survei')
    def test_create_should_register_pertanyaan_once(self, get_survei_mock, register_pertanyaan_mock, register_opsi_jawaban_mock):
        survei_mock = MagicMock(spec=Survei)
        get_survei_mock.configure_mock(return_value=survei_mock)

        self.serializer.create(self.serializer_data)

        register_pertanyaan_mock.assert_called_once_with(
            survei=survei_mock,
            pertanyaan=self.serializer_data.get("pertanyaan"),
            wajib_diisi=self.serializer_data.get("pertanyaan_wajib_diisi")
        )

    @patch('atlas.apps.survei.services.SurveiService.register_opsi_jawaban_skala_linier')
    @patch('atlas.apps.survei.services.SurveiService.register_pertanyaan_skala_linier')
    @patch('atlas.apps.survei.services.SurveiService.get_survei')
    def test_create_should_register_skala_linier_as_requested(
            self, get_survei_mock, register_pertanyaan_mock, register_opsi_jawaban_mock):
        pertanyaan_mock = MagicMock(spec=Pertanyaan)
        register_pertanyaan_mock.configure_mock(return_value=pertanyaan_mock)

        self.serializer.create(self.serializer_data)

        self.assertEqual(register_opsi_jawaban_mock.call_count,
                         self.serializer_data['banyak_skala'])

        register_opsi_jawaban_mock.assert_has_calls(
            [call(pertanyaan=pertanyaan_mock, skala=1),
             call(pertanyaan=pertanyaan_mock, skala=2),
             call(pertanyaan=pertanyaan_mock, skala=3),
             call(pertanyaan=pertanyaan_mock, skala=4),
             call(pertanyaan=pertanyaan_mock, skala=5),
             ])

    @patch('atlas.apps.survei.services.SurveiService.register_opsi_jawaban_skala_linier')
    @patch('atlas.apps.survei.services.SurveiService.register_pertanyaan_skala_linier')
    @patch('atlas.apps.survei.services.SurveiService.get_survei')
    def test_create_should_return_pertanyaan(
            self, get_survei_mock, register_pertanyaan_mock, register_opsi_jawaban_mock):
        pertanyaan_mock = MagicMock(spec=Pertanyaan)
        register_pertanyaan_mock.configure_mock(return_value=pertanyaan_mock)

        return_value = self.serializer.create(self.serializer_data)
        self.assertEqual(return_value.get("pertanyaan"), pertanyaan_mock)

    @patch('atlas.apps.survei.services.SurveiService.register_opsi_jawaban_skala_linier')
    @patch('atlas.apps.survei.services.SurveiService.register_pertanyaan_skala_linier')
    @patch('atlas.apps.survei.services.SurveiService.get_survei')
    def test_create_should_return_opsi_jawaban(
            self, get_survei_mock, register_pertanyaan_mock, register_opsi_jawaban_mock):
        opsi_jawaban_mock = MagicMock(spec=OpsiJawaban)
        register_opsi_jawaban_mock.configure_mock(
            return_value=opsi_jawaban_mock)

        return_value = self.serializer.create(self.serializer_data)
        banyak = self.serializer_data['banyak_skala']

        self.assertEqual(return_value.get("skala_linier"),
                         [opsi_jawaban_mock]*banyak)


class TestJawabanSingkatRequestSerializer(TestCase):

    def setUp(self) -> None:
        self.serializer_data = {
            'survei_id': 1,
            'pertanyaan': 'Siapakah nama panggilan anda?',
            'wajib_diisi': True,
            'jawaban': 'Budi'
        }

        self.serializer = IsianRequestSerializer(
            data=self.serializer_data)

    def test_request_contains_expected_fields(self):
        fields = self.serializer.get_fields()
        self.assertEqual(set(fields), set(
            ['survei_id', 'pertanyaan', 'wajib_diisi', 'jawaban']))

    @patch('atlas.apps.survei.services.SurveiService.get_survei')
    def test_initial_request_is_valid(self, get_survei_mock):
        self.assertTrue(self.serializer.is_valid())

    @patch('atlas.apps.survei.services.SurveiService.get_survei')
    def test_survei_id_is_required(self, get_survei_mock):
        self.serializer_data.pop('survei_id')
        serializer = IsianRequestSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())

    @patch('atlas.apps.survei.services.SurveiService.get_survei')
    def test_pertanyaan_is_required(self, get_survei_mock):
        self.serializer_data.pop('pertanyaan')
        serializer = IsianRequestSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())

    @patch('atlas.apps.survei.services.SurveiService.get_survei')
    def test_validate_called_get_survei_once(self, get_survei_mock):
        self.serializer.is_valid()
        get_survei_mock.assert_called_once()

    @patch('atlas.apps.survei.services.SurveiService.get_survei', Mock(return_value=None))
    def test_validate_should_fail_if_get_survei_return_none(self):
        self.assertFalse(self.serializer.is_valid())

    @patch('atlas.apps.survei.services.SurveiService.get_survei', Mock(return_value=None))
    def test_validate_should_raise_error_if_get_survei_return_none(self):
        self.serializer.is_valid()
        self.assertRaises(serializers.ValidationError)

    @patch('atlas.apps.survei.services.SurveiService.get_survei', Mock(return_value=True))
    def test_validate_should_succeed_if_get_survei_return_some(self):
        self.assertTrue(self.serializer.is_valid())

    @patch('atlas.apps.survei.services.SurveiService.get_survei', Mock(return_value=None))
    def test_validate_survey_id_should_raise_with_correct_message(self):
        with self.assertRaises(serializers.ValidationError) as exc:
            self.serializer.validate_survei_id(1)
        self.assertEqual(str(exc.exception.detail[0]),
                         "Survei dengan id 1 tidak ditemukan")

    @patch('atlas.apps.survei.services.SurveiService.register_opsi_jawaban_isian')
    @patch('atlas.apps.survei.services.SurveiService.register_pertanyaan_isian')
    @patch('atlas.apps.survei.services.SurveiService.get_survei')
    def test_create_should_call_get_survei_once_with_param(self, get_survei_mock, register_pertanyaan_mock, register_opsi_jawaban_mock):
        self.serializer.create(self.serializer_data)
        get_survei_mock.assert_called_once_with(
            self.serializer_data['survei_id'])

    @patch('atlas.apps.survei.services.SurveiService.register_opsi_jawaban_isian')
    @patch('atlas.apps.survei.services.SurveiService.register_pertanyaan_isian')
    @patch('atlas.apps.survei.services.SurveiService.get_survei')
    def test_create_should_register_pertanyaan_once(self, get_survei_mock, register_pertanyaan_mock, register_opsi_jawaban_mock):
        survei_mock = MagicMock(spec=Survei)
        get_survei_mock.configure_mock(return_value=survei_mock)

        self.serializer.create(self.serializer_data)

        register_pertanyaan_mock.assert_called_once_with(
            survei=survei_mock,
            pertanyaan=self.serializer_data.get("pertanyaan"),
            wajib_diisi=self.serializer_data.get("wajib_diisi")
        )

    @patch('atlas.apps.survei.services.SurveiService.register_opsi_jawaban_isian')
    @patch('atlas.apps.survei.services.SurveiService.register_pertanyaan_isian')
    @patch('atlas.apps.survei.services.SurveiService.get_survei')
    def test_create_should_return_pertanyaan(
            self, get_survei_mock, register_pertanyaan_mock, register_opsi_jawaban_mock):
        pertanyaan_mock = MagicMock(spec=Pertanyaan)
        register_pertanyaan_mock.configure_mock(return_value=pertanyaan_mock)

        return_value = self.serializer.create(self.serializer_data)
        self.assertEqual(return_value.get("pertanyaan"), pertanyaan_mock)


class TestRadioButtonRequestSerializer(TestCase):

    def setUp(self) -> None:
        self.serializer_data = {
            'survei_id': 1,
            'pertanyaan': 'Lulusan angkatan berapa Anda?',
            'required': True,
            'option': ["2018", "2019", "2020", "2021", "2022"],
        }
        self.serializer = RadioButtonRequestSerializer(data=self.serializer_data)

    def test_request_contains_expected_fields(self):
        fields = self.serializer.get_fields()
        self.assertEqual(set(fields), set(
            ['survei_id', 'pertanyaan', 'required', 'option']))

    @patch('atlas.apps.survei.services.SurveiService.get_survei')
    def test_initial_request_is_valid(self, get_survei_mock):
        self.assertTrue(self.serializer.is_valid())

    def test_survei_id_is_required(self):
        self.serializer_data.pop('survei_id')
        serializer = RadioButtonRequestSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())

    def test_pertanyaan_is_required(self):
        self.serializer_data.pop('pertanyaan')
        serializer = RadioButtonRequestSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())

    def test_option_is_not_empty(self):
        self.serializer_data['option'] = []
        serializer = SkalaLinierRequestSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())

    @patch('atlas.apps.survei.services.SurveiService.get_survei')
    def test_validate_called_get_survei_once(self, get_survei_mock):
        self.serializer.is_valid()
        get_survei_mock.assert_called_once()

    @patch('atlas.apps.survei.services.SurveiService.get_survei', Mock(return_value=True))
    def test_validate_should_succeed_if_get_survei_return_value(self):
        self.assertTrue(self.serializer.is_valid())

    @patch('atlas.apps.survei.services.SurveiService.get_survei', Mock(return_value=None))
    def test_validate_should_fail_if_get_survei_return_none(self):
        self.assertFalse(self.serializer.is_valid())

    @patch('atlas.apps.survei.services.SurveiService.get_survei', Mock(return_value=None))
    def test_validate_should_raise_error_if_get_survei_return_none(self):
        self.serializer.is_valid()
        self.assertRaises(serializers.ValidationError)

    @patch('atlas.apps.survei.services.SurveiService.get_survei', Mock(return_value=None))
    def test_validate_survey_id_should_raise_with_correct_message(self):
        with self.assertRaises(serializers.ValidationError) as exc:
            self.serializer.validate_survei_id(1)
        self.assertEqual(str(exc.exception.detail[0]), "Survei with id 1 does not exist")

    @patch('atlas.apps.survei.services.SurveiService.register_opsi_jawaban_radiobutton')
    @patch('atlas.apps.survei.services.SurveiService.register_pertanyaan_radiobutton')
    @patch('atlas.apps.survei.services.SurveiService.get_survei')
    def test_create_should_call_get_survei_once_with_param(self, get_survei_mock, register_pertanyaan_mock, register_opsi_jawaban_mock):
        self.serializer.create(self.serializer_data)
        get_survei_mock.assert_called_once_with(self.serializer_data['survei_id'])

    @patch('atlas.apps.survei.services.SurveiService.register_opsi_jawaban_radiobutton')
    @patch('atlas.apps.survei.services.SurveiService.register_pertanyaan_radiobutton')
    @patch('atlas.apps.survei.services.SurveiService.get_survei')
    def test_create_should_register_pertanyaan_once(self, get_survei_mock, register_pertanyaan_mock, register_opsi_jawaban_mock):
        survei_mock = MagicMock(spec=Survei)
        get_survei_mock.configure_mock(return_value=survei_mock)
        self.serializer.create(self.serializer_data)
        register_pertanyaan_mock.assert_called_once_with(
            survei=survei_mock,
            pertanyaan=self.serializer_data.get("pertanyaan"),
            wajib_diisi=self.serializer_data.get("required"))

    @patch('atlas.apps.survei.services.SurveiService.register_opsi_jawaban_radiobutton')
    @patch('atlas.apps.survei.services.SurveiService.register_pertanyaan_radiobutton')
    @patch('atlas.apps.survei.services.SurveiService.get_survei')
    def test_create_should_register_radiobutton_as_requested(self, get_survei_mock, register_pertanyaan_mock, register_opsi_jawaban_mock):
        pertanyaan_mock = MagicMock(spec=Pertanyaan)
        register_pertanyaan_mock.configure_mock(return_value=pertanyaan_mock)
        self.serializer.create(self.serializer_data)
        self.assertEqual(register_opsi_jawaban_mock.call_count, len(self.serializer_data['option']))
        register_opsi_jawaban_mock.assert_has_calls(
            [call(pertanyaan=pertanyaan_mock, pilihan_jawaban="2018"),
             call(pertanyaan=pertanyaan_mock, pilihan_jawaban="2019"),
             call(pertanyaan=pertanyaan_mock, pilihan_jawaban="2020"),
             call(pertanyaan=pertanyaan_mock, pilihan_jawaban="2021"),
             call(pertanyaan=pertanyaan_mock, pilihan_jawaban="2022"),])

    @patch('atlas.apps.survei.services.SurveiService.register_opsi_jawaban_radiobutton')
    @patch('atlas.apps.survei.services.SurveiService.register_pertanyaan_radiobutton')
    @patch('atlas.apps.survei.services.SurveiService.get_survei')
    def test_create_should_return_pertanyaan(self, get_survei_mock, register_pertanyaan_mock, register_opsi_jawaban_mock):
        pertanyaan_mock = MagicMock(spec=Pertanyaan)
        register_pertanyaan_mock.configure_mock(return_value=pertanyaan_mock)
        returned_create = self.serializer.create(self.serializer_data)
        self.assertEqual(returned_create.get("pertanyaan"), pertanyaan_mock)

    @patch('atlas.apps.survei.services.SurveiService.register_opsi_jawaban_radiobutton')
    @patch('atlas.apps.survei.services.SurveiService.register_pertanyaan_radiobutton')
    @patch('atlas.apps.survei.services.SurveiService.get_survei')
    def test_create_should_return_opsi_jawaban(self, get_survei_mock, register_pertanyaan_mock, register_opsi_jawaban_mock):
        options_quantity = self.serializer_data["options"]
        opsi_jawaban_mock = MagicMock(spec=OpsiJawaban)*options_quantity
        register_opsi_jawaban_mock.configure_mock(return_value=opsi_jawaban_mock)
        returned_create = self.serializer.create(self.serializer_data)
        self.assertEqual(returned_create.get("opsi_jawaban"), opsi_jawaban_mock)
