import uuid
import json

from django.urls import reverse
from django.http import QueryDict

from rest_framework import status
from atlas.libs.test import RestTestCase
from atlas.apps.validator import constants

valid_fields = (
    'npm',
    'nama',
    'tglLahir',
    'kotaLahir',
    'nmOrg',
    'angkatan',
    'alamat',
    'statusTerakhirMhs'
)

invalid_fields = (
    'isValid',
)


class TestWithIntegrationTestAlumniValidationView(RestTestCase):

    def setUp(self) -> None:
        self.user = RestTestCase.create_admin()
        self.authenticate(self.user)

    def test_complete_alumni_valid_with_npm_success(self):
        url = reverse('alumni_validation')
        data = {
            "npm": "1606918055",
            "nama": "Wisnu Pramadhitya",
            "tglLahir": "1998-01-14",
            "angkatan": 2016,
            "nmOrg": "Sistem Informasi",
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get('is_valid'))

        content = json.loads(response.content)
        for fd in valid_fields:
            self.assertIn(fd, content)

    def test_complete_alumni_valid_with_npm_partial_query_success(self):
        q = QueryDict(mutable=True)
        q.setlist('fields', [constants.C_UI_NAME_FIELD, constants.C_UI_ORG])
        query_string = q.urlencode()
        url = f'{reverse("alumni_validation")}?{query_string}'

        data = {
            "npm": "1606918055",
            "nama": "Wisnu Pramadhitya",
            "tglLahir": "1998-01-14",
            "angkatan": 2016,
            "nmOrg": "Sistem Informasi",
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get('is_valid'))

        content = json.loads(response.content)
        for fd in valid_fields:
            self.assertIn(fd, content)

    def test_alumni_valid_with_npm_partial_query_not_valid(self):
        q = QueryDict(mutable=True)
        q.setlist('fields', [constants.C_UI_NAME_FIELD, constants.C_UI_ORG])
        query_string = q.urlencode()
        url = f'{reverse("alumni_validation")}?{query_string}'

        data = {
            "npm": "1606918055",
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data.get('is_valid'))

        content = json.loads(response.content)
        for fd in invalid_fields:
            self.assertIn(fd, content)
        for fd in valid_fields:
            self.assertNotIn(fd, content)

    def test_complete_alumni_valid_with_npm_not_found(self):
        q = QueryDict(mutable=True)
        q.setlist('fields', [constants.C_UI_NAME_FIELD, constants.C_UI_ORG])
        query_string = q.urlencode()
        url = f'{reverse("alumni_validation")}?{query_string}'

        data = {
            "npm": "1",
            "nama": "Wisnu Pramadhitya",
            "tglLahir": "1998-01-14",
            "angkatan": 2016,
            "nmOrg": "Sistem Informasi",
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data.get('is_valid'))

        content = json.loads(response.content)
        for fd in invalid_fields:
            self.assertIn(fd, content)
        for fd in valid_fields:
            self.assertNotIn(fd, content)

    def test_complete_alumni_valid_without_identifier(self):
        url = reverse("alumni_validation")
        data = {
            "tglLahir": "1998-01-14",
            "angkatan": 2016,
            "nmOrg": "Sistem Informasi",
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        content = json.loads(response.content)
        for fd in invalid_fields:
            self.assertIn(fd, content)
        for fd in valid_fields:
            self.assertNotIn(fd, content)

    def test_complete_alumni_valid_with_name(self):
        url = reverse("alumni_validation")
        data = {
            "nama": "Wisnu Pramadhitya",
            "tglLahir": "1998-01-14",
            "angkatan": 2016,
            "nmOrg": "Sistem Informasi",
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get('is_valid'))

        content = json.loads(response.content)
        for fd in valid_fields:
            self.assertIn(fd, content)

    def test_alumni_valid_with_name_without_query(self):
        url = reverse("alumni_validation")
        data = {
            "nama": "Wisnu",
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data.get('is_valid'))

        content = json.loads(response.content)
        for fd in invalid_fields:
            self.assertIn(fd, content)
        for fd in valid_fields:
            self.assertNotIn(fd, content)

    def test_alumni_valid_with_name_with_query(self):
        q = QueryDict(mutable=True)
        q.setlist('fields', [constants.C_UI_NAME_FIELD])
        query_string = q.urlencode()
        url = f'{reverse("alumni_validation")}?{query_string}'
        data = {
            "nama": "Wisnu Pramadhitya",
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get('is_valid'))

        content = json.loads(response.content)
        for fd in valid_fields:
            self.assertIn(fd, content)

        q = QueryDict(mutable=True)
        q.setlist('fields', [constants.C_UI_NAME_FIELD, constants.C_UI_ORG])
        query_string = q.urlencode()
        url = f'{reverse("alumni_validation")}?{query_string}'
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data.get('is_valid'))

        content = json.loads(response.content)
        for fd in invalid_fields:
            self.assertIn(fd, content)
        for fd in valid_fields:
            self.assertNotIn(fd, content)

    def test_alumni_valid_with_name_not_found(self):
        q = QueryDict(mutable=True)
        q.setlist('fields', [constants.C_UI_NAME_FIELD])
        query_string = q.urlencode()
        url = f'{reverse("alumni_validation")}?{query_string}'
        data = {
            "nama": 'ajwdawdahwdkjahdkj',
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data.get('is_valid'))

        content = json.loads(response.content)
        for fd in invalid_fields:
            self.assertIn(fd, content)
        for fd in valid_fields:
            self.assertNotIn(fd, content)

    def test_alumni_valid_with_npm_or_name_filled_with_unknown(self):
        '''
        Regression only to take a note of the behavior of csui
        :return:
        '''
        url = reverse("alumni_validation")
        data = {
            "nama": str(uuid.uuid4()),
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        content = json.loads(response.content)
        for fd in invalid_fields:
            self.assertIn(fd, content)
        for fd in valid_fields:
            self.assertNotIn(fd, content)

        data = {
            "npm": str(uuid.uuid4()),
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        content = json.loads(response.content)
        for fd in invalid_fields:
            self.assertIn(fd, content)
