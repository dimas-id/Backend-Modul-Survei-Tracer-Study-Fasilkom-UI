from atlas.apps.validator import constants

class AlumniValidation:

    def __init__(self, **kwargs):
        self.nama = kwargs.get(constants.C_UI_NAME_FIELD)
        self.npm = kwargs.get(constants.C_UI_NPM_FIELD)
        self.nm_org = kwargs.get(constants.C_UI_ORG)
        self.angkatan = kwargs.get(constants.C_UI_CLASS_YEAR_FIELD)

        self.kota_lahir = kwargs.get(constants.C_UI_CITY_BIRTH)
        self.tgl_lahir = kwargs.get(constants.C_UI_BIRTHDATE_FIELD)
        self.alamat = kwargs.get(constants.C_UI_ADDRESS)
        self.status_terakhir_mhs = kwargs.get(constants.C_UI_STATUS)

        self.__is_valid__ = kwargs.get('is_valid', False)

    def has_npm(self):
        return self.npm is not None

    def set_valid(self):
        self.__is_valid__ = True

    def set_invalid(self):
        self.__is_valid__ = False

    @property
    def is_valid(self):
        return self.__is_valid__

    @property
    def data(self):
        fields = (
            constants.C_UI_NAME_FIELD,
            constants.C_UI_ADDRESS,
            constants.C_UI_BIRTHDATE_FIELD,
            constants.C_UI_CITY_BIRTH,
            constants.C_UI_ORG,
            constants.C_UI_CLASS_YEAR_FIELD,
            constants.C_UI_NPM_FIELD,
            'is_valid'
        )

        raw = {}
        for fd in fields:
            raw[fd] = getattr(self, fd, None)
        return raw
