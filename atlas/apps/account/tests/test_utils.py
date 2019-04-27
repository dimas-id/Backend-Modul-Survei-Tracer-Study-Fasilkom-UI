from django.test import TestCase

from atlas.apps.account.utils import extract_alumni_data


class UtilsTest(TestCase):

    def setUp(self) -> None:
        self.mhs_data = {
            "url"       : "https://api.cs.ui.ac.id/siakngcs/mahasiswa/0806316915/",
            "npm"       : "0806316915",
            "nama"      : "NUR FITRIAH AYUNING BUDI, M.H",
            "alamat_mhs": "Jl Stasiun 32 Pondok Cina Depok Jawa Barat",
            "kd_pos_mhs": "63138",
            "kota_lahir": "Madiun",
            "tgl_lahir" : "1990-09-08",
            "program"   : [
                {
                    "url"      : "https://api.cs.ui.ac.id/siakngcs/program/21729/",
                    "periode"  : {
                        "url"  : "https://api.cs.ui.ac.id/siakngcs/periode/19/",
                        "term" : 1,
                        "tahun": 2012
                    },
                    "kd_org"   : "06.00.12.01",
                    "nm_org"   : "Sistem Informasi",
                    "nm_prg"   : "S1 Reguler",
                    "angkatan" : 2008,
                    "nm_status": "Lulus",
                    "kd_status": "5"
                },
                {
                    "url"      : "https://api.cs.ui.ac.id/siakngcs/program/19934/",
                    "periode"  : {
                        "url"  : "https://api.cs.ui.ac.id/siakngcs/periode/18/",
                        "term" : 3,
                        "tahun": 2011
                    },
                    "kd_org"   : "06.00.12.01",
                    "nm_org"   : "Sistem Informasi",
                    "nm_prg"   : "S1 Reguler",
                    "angkatan" : 2008,
                    "nm_status": "Kosong",
                    "kd_status": "0"
                },
                {
                    "url"      : "https://api.cs.ui.ac.id/siakngcs/program/18865/",
                    "periode"  : {
                        "url"  : "https://api.cs.ui.ac.id/siakngcs/periode/17/",
                        "term" : 2,
                        "tahun": 2011
                    },
                    "kd_org"   : "06.00.12.01",
                    "nm_org"   : "Sistem Informasi",
                    "nm_prg"   : "S1 Reguler",
                    "angkatan" : 2008,
                    "nm_status": "Aktif",
                    "kd_status": "1"
                },
                {
                    "url"      : "https://api.cs.ui.ac.id/siakngcs/program/17237/",
                    "periode"  : {
                        "url"  : "https://api.cs.ui.ac.id/siakngcs/periode/16/",
                        "term" : 1,
                        "tahun": 2011
                    },
                    "kd_org"   : "06.00.12.01",
                    "nm_org"   : "Sistem Informasi",
                    "nm_prg"   : "S1 Reguler",
                    "angkatan" : 2008,
                    "nm_status": "Aktif",
                    "kd_status": "1"
                },
                {
                    "url"      : "https://api.cs.ui.ac.id/siakngcs/program/15580/",
                    "periode"  : {
                        "url"  : "https://api.cs.ui.ac.id/siakngcs/periode/15/",
                        "term" : 3,
                        "tahun": 2010
                    },
                    "kd_org"   : "06.00.12.01",
                    "nm_org"   : "Sistem Informasi",
                    "nm_prg"   : "S1 Reguler",
                    "angkatan" : 2008,
                    "nm_status": "Kosong",
                    "kd_status": "0"
                },
                {
                    "url"      : "https://api.cs.ui.ac.id/siakngcs/program/14596/",
                    "periode"  : {
                        "url"  : "https://api.cs.ui.ac.id/siakngcs/periode/14/",
                        "term" : 2,
                        "tahun": 2010
                    },
                    "kd_org"   : "06.00.12.01",
                    "nm_org"   : "Sistem Informasi",
                    "nm_prg"   : "S1 Reguler",
                    "angkatan" : 2008,
                    "nm_status": "Aktif",
                    "kd_status": "1"
                },
                {
                    "url"      : "https://api.cs.ui.ac.id/siakngcs/program/13085/",
                    "periode"  : {
                        "url"  : "https://api.cs.ui.ac.id/siakngcs/periode/13/",
                        "term" : 1,
                        "tahun": 2010
                    },
                    "kd_org"   : "06.00.12.01",
                    "nm_org"   : "Sistem Informasi",
                    "nm_prg"   : "S1 Reguler",
                    "angkatan" : 2008,
                    "nm_status": "Aktif",
                    "kd_status": "1"
                },
                {
                    "url"      : "https://api.cs.ui.ac.id/siakngcs/program/11553/",
                    "periode"  : {
                        "url"  : "https://api.cs.ui.ac.id/siakngcs/periode/12/",
                        "term" : 3,
                        "tahun": 2009
                    },
                    "kd_org"   : "06.00.12.01",
                    "nm_org"   : "Sistem Informasi",
                    "nm_prg"   : "S1 Reguler",
                    "angkatan" : 2008,
                    "nm_status": "Aktif",
                    "kd_status": "1"
                },
                {
                    "url"      : "https://api.cs.ui.ac.id/siakngcs/program/10628/",
                    "periode"  : {
                        "url"  : "https://api.cs.ui.ac.id/siakngcs/periode/11/",
                        "term" : 2,
                        "tahun": 2009
                    },
                    "kd_org"   : "06.00.12.01",
                    "nm_org"   : "Sistem Informasi",
                    "nm_prg"   : "S1 Reguler",
                    "angkatan" : 2008,
                    "nm_status": "Aktif",
                    "kd_status": "1"
                },
                {
                    "url"      : "https://api.cs.ui.ac.id/siakngcs/program/9221/",
                    "periode"  : {
                        "url"  : "https://api.cs.ui.ac.id/siakngcs/periode/10/",
                        "term" : 1,
                        "tahun": 2009
                    },
                    "kd_org"   : "06.00.12.01",
                    "nm_org"   : "Sistem Informasi",
                    "nm_prg"   : "S1 Reguler",
                    "angkatan" : 2008,
                    "nm_status": "Aktif",
                    "kd_status": "1"
                },
                {
                    "url"      : "https://api.cs.ui.ac.id/siakngcs/program/7852/",
                    "periode"  : {
                        "url"  : "https://api.cs.ui.ac.id/siakngcs/periode/9/",
                        "term" : 3,
                        "tahun": 2008
                    },
                    "kd_org"   : "06.00.12.01",
                    "nm_org"   : "Sistem Informasi",
                    "nm_prg"   : "S1 Reguler",
                    "angkatan" : 2008,
                    "nm_status": "Aktif",
                    "kd_status": "1"
                },
                {
                    "url"      : "https://api.cs.ui.ac.id/siakngcs/program/7152/",
                    "periode"  : {
                        "url"  : "https://api.cs.ui.ac.id/siakngcs/periode/8/",
                        "term" : 2,
                        "tahun": 2008
                    },
                    "kd_org"   : "06.00.12.01",
                    "nm_org"   : "Sistem Informasi",
                    "nm_prg"   : "S1 Reguler",
                    "angkatan" : 2008,
                    "nm_status": "Aktif",
                    "kd_status": "1"
                },
                {
                    "url"      : "https://api.cs.ui.ac.id/siakngcs/program/6004/",
                    "periode"  : {
                        "url"  : "https://api.cs.ui.ac.id/siakngcs/periode/7/",
                        "term" : 1,
                        "tahun": 2008
                    },
                    "kd_org"   : "06.00.12.01",
                    "nm_org"   : "Sistem Informasi",
                    "nm_prg"   : "S1 Reguler",
                    "angkatan" : 2008,
                    "nm_status": "Aktif",
                    "kd_status": "1"
                }
            ]
        }

    def test_extract_alumni_(self):
        extracted_data = extract_alumni_data(dict(self.mhs_data))
        self.assertEqual(type(extracted_data), tuple)
        self.assertEqual(extracted_data[0], 'NUR FITRIAH AYUNING BUDI, M.H')
        self.assertEqual(extracted_data[1], '0806316915')
        self.assertEqual(extracted_data[2], '1990-09-08')
        self.assertEqual(extracted_data[3], 'S1-SI')
        self.assertEqual(extracted_data[4], 2008)
