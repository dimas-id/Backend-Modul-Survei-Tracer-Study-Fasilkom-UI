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
        :rtype: tuple(dict, boolean)
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
        uri = f'/mahasiswa/nama/{nama}/'
        return self.get_client().get(uri=uri)


class SisidangCS(AbstractCSUIClient, AbstractClient):

    class Meta:
        always_use_production = True
        is_camelized = False
        client_url = {
            'production': 'https://sidang.cs.ui.ac.id',
            'development': 'http://3d7c0bf8-e0d3-43bc-846c-462317f587ee.mock.pstmn.io/sisidang'
        }
class GraduatedStudentManager(AbstractClientManager):

    client = SisidangCS()

    def get_all_student_by_year_and_term(self, year: str, term: str):
        """
        this assuming that the api not change to pagination.
        :param year: tahun lulus (ex: 2021/2022)
        :type year: str
        :param term: term lulus (ex: 2)
        :type year: str
        :return: return list of mahasiswa with given year and term and success status
        :rtype: tuple(dict, boolean)
        """ 
        uri = f'/daftar-mahasiswa-sidang?tahun={year}&term={term}'
        return self.get_client().get(uri=uri)
