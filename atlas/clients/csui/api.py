from django.conf import settings
from atlas.libs.client import AbstractClient, AbstractClientManager


class SiakNGCS(AbstractClient):

    # TODO munkgin nanti perlu menyematkan di header api keynya

    class Meta:
        always_use_production = False
        is_camelized = False
        client_url = {
            'production': 'https://api.cs.ui.ac.id/siakngcs',
            'development': 'https://fc8ae1b3-1a66-4b64-863b-b23f682ecce5.mock.pstmn.io'
        }


class StudentManager(AbstractClientManager):
    client = SiakNGCS()

    def get_student_by_npm(self, npm):
        uri = f'/mahasiswa/{npm}'
        return self.get_client().get(uri=uri)

