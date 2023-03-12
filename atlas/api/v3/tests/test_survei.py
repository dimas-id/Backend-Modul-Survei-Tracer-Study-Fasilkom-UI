from atlas.apps.account.models import User
from rest_framework.test import APIRequestFactory, APITestCase
from django.urls import reverse
from rest_framework import status
from django.urls import reverse


class TestSurveiModels(APITestCase):

    def setUp(self):
        user_data = {
            'first_name': "indra",
            'last_name': 'mahaarta',
            'email': 'i@gmail.com'
        }

        self.factory = APIRequestFactory()
        User.objects.create(**user_data)


    def authenticate(self):
        data = {
            'email': 'indra@csui.com',
            'password': 'indraashuj82890923',
            'firstName': 'mhrt',
            'lastName': 'indr',
            'birthdate': '1998-01-14',
            'linkedinUrl': 'https://linkedin.com/in/indra'
        }

        uri = reverse('account_register_v2')
        response = self.client.post(path=uri, data=data)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + response.data['access'])


    def test_valid_api_regiester_survei(self):
        request = self.factory.post(path="/api/v3/survei/create", )
        user = User.objects.get(first_name="indra")
        request.user = user
        data = {
            "nama": "Survei 03",
            "deskripsi": "lorem ipsum keren"
        }
        self.authenticate()
        response = self.client.post(
            "/api/v3/survei/create", data=data, request=request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_invalid_api_regiester_survei(self):
        request = self.factory.post(path="/api/v3/survei/create", )
        user = User.objects.get(first_name="indra")
        request.user = user
        data = {
            "nama": "Survei 03"
        }
        self.authenticate()
        response = self.client.post(
            "/api/v3/survei/create", data=data, request=request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_valid_get_survei(self):
        request = self.factory.post(path="/api/v3/survei/list", )
        user = User.objects.get(first_name="indra")
        request.user = user
        self.authenticate()
        response = self.client.get(
            "/api/v3/survei/list", request=request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
