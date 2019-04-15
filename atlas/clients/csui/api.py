from django.conf import settings
from atlas.libs.client import AbstractClient, AbstractClientManager, HTTPBasicAuth


class AbstractCSUIClient:
    auth = HTTPBasicAuth(settings.CSUI_USERNAME, settings.CSUI_PASSWORD)


class SiakNGCS(AbstractCSUIClient, AbstractClient):

    class Meta:
        always_use_production = True
        is_camelized = False
        client_url = {
            'production': 'https://api.cs.ui.ac.id/siakngcs',
            'development': 'https://fc8ae1b3-1a66-4b64-863b-b23f682ecce5.mock.pstmn.io'
        }


class StudentManager(AbstractClientManager):

    client = SiakNGCS()

    def get_student_by_npm(self, npm: str):
        """
        this assuming that the api not change to pagination.
        :param nama: mahasiswa npm
        :type arg1: str
        :return: return mahasiswa with given name and success status
        :rtype: tuple(list, boolean)
        """
        uri = f'/mahasiswa/{npm}/'
        return self.get_client().get(uri=uri)

    def get_students_by_name(self, nama: str):
        """
        this assuming that the api not change to pagination.
        :param nama: mahasiswa name
        :type arg1: str
        :return: return list of mahasiswa with given name and success status
        :rtype: tuple(list, boolean)
        """
        uri = f'/siakngcs/mahasiswa/nama/{nama}/'
        return self.get_client().get(uri=uri)
