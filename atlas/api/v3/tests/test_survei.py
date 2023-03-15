from atlas.apps.account.models import User
from rest_framework.test import APIRequestFactory, APITestCase
from django.urls import reverse
from rest_framework import status
from django.urls import reverse

from atlas.libs.test import RestTestCase


class TestSurveiModels(RestTestCase):

    CREATE_SURVEI_URL = "/api/v3/survei/create"
    LIST_SURVEI_URL = "/api/v3/survei/list"

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = RestTestCase.create_admin()

    def test_valid_api_regiester_survei(self):
        request = self.factory.post(path=self.CREATE_SURVEI_URL)
        self.authenticate(self.user)
        request.user = self.user
        data = {
            "nama": "Survei 03",
            "deskripsi": "lorem ipsum keren"
        }
        response = self.client.post(
            self.CREATE_SURVEI_URL, data=data, request=request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_api_regiester_survei(self):
        request = self.factory.post(path=self.CREATE_SURVEI_URL)
        self.authenticate(self.user)
        request.user = self.user
        data = {
            "nama": "Survei 03"
        }
        response = self.client.post(
            self.CREATE_SURVEI_URL, data=data, request=request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_get_survei(self):
        request = self.factory.post(path=self.LIST_SURVEI_URL)
        self.authenticate(self.user)
        request.user = self.user
        response = self.client.get(
            self.LIST_SURVEI_URL, request=request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_survei_not_authorized(self):
        request = self.factory.post(path=self.LIST_SURVEI_URL)
        request.user = self.user

        response = self.client.get(
            self.LIST_SURVEI_URL, request=request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
