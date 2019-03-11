from atlas.common.client import AbstractClient, AbstractClientManager


class CsuiClient(AbstractClient):

    # TODO munkgin nanti perlu menyematkan di header api keynya

    class Meta:
        always_use_production = False
        client_url = {
            'production': '',
            'development': 'https://fc8ae1b3-1a66-4b64-863b-b23f682ecce5.mock.pstmn.io'
        }


class StudentManager(AbstractClientManager):
    client = CsuiClient()

    def get_student_by_npm(self, npm):
        uri = f'/mahasiswa/{npm}'
        return self.get_client().get(uri=uri)

    def get_students_by_class(self, year):
        uri = f'/mahasiswa?year={year}'
        return self.get_client().get(uri=uri)
