from django.test import TestCase

from atlas.apps.account.utils import extract_alumni_data, validate_alumni_data
from atlas.apps.account.models import User


class UtilsTest(TestCase):

    def test_extract_alumni_(self):
        mhs_data = {
            "url": "https://api.cs.ui.ac.id/siakngcs/mahasiswa/0806316915/",
            "npm": "0806316915",
            "nama": "NUR FITRIAH AYUNING BUDI, M.H",
            "alamat_mhs": "Jl Stasiun 32 Pondok Cina Depok Jawa Barat",
            "kd_pos_mhs": "63138",
            "kota_lahir": "Madiun",
            "tgl_lahir": "1990-09-08",
            "program": [
                {
                    "url": "https://api.cs.ui.ac.id/siakngcs/program/21729/",
                    "periode": {
                        "url": "https://api.cs.ui.ac.id/siakngcs/periode/19/",
                        "term": 1,
                        "tahun": 2012
                    },
                    "kd_org": "06.00.12.01",
                    "nm_org": "Sistem Informasi",
                    "nm_prg": "S1 Reguler",
                    "angkatan": 2008,
                    "nm_status": "Lulus",
                    "kd_status": "5"
                },
                {
                    "url": "https://api.cs.ui.ac.id/siakngcs/program/19934/",
                    "periode": {
                        "url": "https://api.cs.ui.ac.id/siakngcs/periode/18/",
                        "term": 3,
                        "tahun": 2011
                    },
                    "kd_org": "06.00.12.01",
                    "nm_org": "Sistem Informasi",
                    "nm_prg": "S1 Reguler",
                    "angkatan": 2008,
                    "nm_status": "Kosong",
                    "kd_status": "0"
                },
                {
                    "url": "https://api.cs.ui.ac.id/siakngcs/program/18865/",
                    "periode": {
                        "url": "https://api.cs.ui.ac.id/siakngcs/periode/17/",
                        "term": 2,
                        "tahun": 2011
                    },
                    "kd_org": "06.00.12.01",
                    "nm_org": "Sistem Informasi",
                    "nm_prg": "S1 Reguler",
                    "angkatan": 2008,
                    "nm_status": "Aktif",
                    "kd_status": "1"
                },
                {
                    "url": "https://api.cs.ui.ac.id/siakngcs/program/17237/",
                    "periode": {
                        "url": "https://api.cs.ui.ac.id/siakngcs/periode/16/",
                        "term": 1,
                        "tahun": 2011
                    },
                    "kd_org": "06.00.12.01",
                    "nm_org": "Sistem Informasi",
                    "nm_prg": "S1 Reguler",
                    "angkatan": 2008,
                    "nm_status": "Aktif",
                    "kd_status": "1"
                },
                {
                    "url": "https://api.cs.ui.ac.id/siakngcs/program/15580/",
                    "periode": {
                        "url": "https://api.cs.ui.ac.id/siakngcs/periode/15/",
                        "term": 3,
                        "tahun": 2010
                    },
                    "kd_org": "06.00.12.01",
                    "nm_org": "Sistem Informasi",
                    "nm_prg": "S1 Reguler",
                    "angkatan": 2008,
                    "nm_status": "Kosong",
                    "kd_status": "0"
                },
                {
                    "url": "https://api.cs.ui.ac.id/siakngcs/program/14596/",
                    "periode": {
                        "url": "https://api.cs.ui.ac.id/siakngcs/periode/14/",
                        "term": 2,
                        "tahun": 2010
                    },
                    "kd_org": "06.00.12.01",
                    "nm_org": "Sistem Informasi",
                    "nm_prg": "S1 Reguler",
                    "angkatan": 2008,
                    "nm_status": "Aktif",
                    "kd_status": "1"
                },
                {
                    "url": "https://api.cs.ui.ac.id/siakngcs/program/13085/",
                    "periode": {
                        "url": "https://api.cs.ui.ac.id/siakngcs/periode/13/",
                        "term": 1,
                        "tahun": 2010
                    },
                    "kd_org": "06.00.12.01",
                    "nm_org": "Sistem Informasi",
                    "nm_prg": "S1 Reguler",
                    "angkatan": 2008,
                    "nm_status": "Aktif",
                    "kd_status": "1"
                },
                {
                    "url": "https://api.cs.ui.ac.id/siakngcs/program/11553/",
                    "periode": {
                        "url": "https://api.cs.ui.ac.id/siakngcs/periode/12/",
                        "term": 3,
                        "tahun": 2009
                    },
                    "kd_org": "06.00.12.01",
                    "nm_org": "Sistem Informasi",
                    "nm_prg": "S1 Reguler",
                    "angkatan": 2008,
                    "nm_status": "Aktif",
                    "kd_status": "1"
                },
                {
                    "url": "https://api.cs.ui.ac.id/siakngcs/program/10628/",
                    "periode": {
                        "url": "https://api.cs.ui.ac.id/siakngcs/periode/11/",
                        "term": 2,
                        "tahun": 2009
                    },
                    "kd_org": "06.00.12.01",
                    "nm_org": "Sistem Informasi",
                    "nm_prg": "S1 Reguler",
                    "angkatan": 2008,
                    "nm_status": "Aktif",
                    "kd_status": "1"
                },
                {
                    "url": "https://api.cs.ui.ac.id/siakngcs/program/9221/",
                    "periode": {
                        "url": "https://api.cs.ui.ac.id/siakngcs/periode/10/",
                        "term": 1,
                        "tahun": 2009
                    },
                    "kd_org": "06.00.12.01",
                    "nm_org": "Sistem Informasi",
                    "nm_prg": "S1 Reguler",
                    "angkatan": 2008,
                    "nm_status": "Aktif",
                    "kd_status": "1"
                },
                {
                    "url": "https://api.cs.ui.ac.id/siakngcs/program/7852/",
                    "periode": {
                        "url": "https://api.cs.ui.ac.id/siakngcs/periode/9/",
                        "term": 3,
                        "tahun": 2008
                    },
                    "kd_org": "06.00.12.01",
                    "nm_org": "Sistem Informasi",
                    "nm_prg": "S1 Reguler",
                    "angkatan": 2008,
                    "nm_status": "Aktif",
                    "kd_status": "1"
                },
                {
                    "url": "https://api.cs.ui.ac.id/siakngcs/program/7152/",
                    "periode": {
                        "url": "https://api.cs.ui.ac.id/siakngcs/periode/8/",
                        "term": 2,
                        "tahun": 2008
                    },
                    "kd_org": "06.00.12.01",
                    "nm_org": "Sistem Informasi",
                    "nm_prg": "S1 Reguler",
                    "angkatan": 2008,
                    "nm_status": "Aktif",
                    "kd_status": "1"
                },
                {
                    "url": "https://api.cs.ui.ac.id/siakngcs/program/6004/",
                    "periode": {
                        "url": "https://api.cs.ui.ac.id/siakngcs/periode/7/",
                        "term": 1,
                        "tahun": 2008
                    },
                    "kd_org": "06.00.12.01",
                    "nm_org": "Sistem Informasi",
                    "nm_prg": "S1 Reguler",
                    "angkatan": 2008,
                    "nm_status": "Aktif",
                    "kd_status": "1"
                }
            ]
        }
        extracted_data = extract_alumni_data(mhs_data)
        self.assertEqual(type(extracted_data), tuple)
        self.assertEqual(extracted_data[0], 'NUR FITRIAH AYUNING BUDI, M.H')
        self.assertEqual(extracted_data[1], '0806316915')
        self.assertEqual(extracted_data[2], '1990-09-08')
        self.assertEqual(extracted_data[3], 'S1-SI')
        self.assertEqual(extracted_data[4], 2008)

    def test_extract_alumni_and_validate(self):
        mhs_data = {'url': 'https://api.cs.ui.ac.id/siakngcs/mahasiswa/1606918055/', 'npm': '1606918055', 'nama': 'Wisnu Pramadhitya Ramadhan', 'alamat_mhs': 'Jl Amonia I Blok L-12 Kavling Pupuk Kujang', 'kd_pos_mhs': '16422', 'kota_lahir': 'Surabaya', 'tgl_lahir': '1998-01-14', 'program': [{'url': 'https://api.cs.ui.ac.id/siakngcs/program/1751028/', 'periode': {'url': 'https://api.cs.ui.ac.id/siakngcs/periode/38/', 'term': 2, 'tahun': 2018}, 'kd_org': '08.00.12.01', 'nm_org': 'Sistem Informasi', 'nm_prg': 'S1 Paralel', 'angkatan': 2016, 'nm_status': 'Aktif', 'kd_status': '1'}, {'url': 'https://api.cs.ui.ac.id/siakngcs/program/1748930/', 'periode': {'url': 'https://api.cs.ui.ac.id/siakngcs/periode/37/', 'term': 1, 'tahun': 2018}, 'kd_org': '08.00.12.01', 'nm_org': 'Sistem Informasi', 'nm_prg': 'S1 Paralel', 'angkatan': 2016, 'nm_status': 'Aktif', 'kd_status': '1'}, {'url': 'https://api.cs.ui.ac.id/siakngcs/program/1270974/', 'periode': {'url': 'https://api.cs.ui.ac.id/siakngcs/periode/36/', 'term': 3, 'tahun': 2017}, 'kd_org': '08.00.12.01', 'nm_org': 'Sistem Informasi', 'nm_prg': 'S1 Paralel', 'angkatan': 2016, 'nm_status': 'Kosong', 'kd_status': '0'}, {'url': 'https://api.cs.ui.ac.id/siakngcs/program/1269703/', 'periode': {
            'url': 'https://api.cs.ui.ac.id/siakngcs/periode/35/', 'term': 2, 'tahun': 2017}, 'kd_org': '08.00.12.01', 'nm_org': 'Sistem Informasi', 'nm_prg': 'S1 Paralel', 'angkatan': 2016, 'nm_status': 'Aktif', 'kd_status': '1'}, {'url': 'https://api.cs.ui.ac.id/siakngcs/program/1267681/', 'periode': {'url': 'https://api.cs.ui.ac.id/siakngcs/periode/34/', 'term': 1, 'tahun': 2017}, 'kd_org': '08.00.12.01', 'nm_org': 'Sistem Informasi', 'nm_prg': 'S1 Paralel', 'angkatan': 2016, 'nm_status': 'Aktif', 'kd_status': '1'}, {'url': 'https://api.cs.ui.ac.id/siakngcs/program/45168/', 'periode': {'url': 'https://api.cs.ui.ac.id/siakngcs/periode/33/', 'term': 3, 'tahun': 2016}, 'kd_org': '08.00.12.01', 'nm_org': 'Sistem Informasi', 'nm_prg': 'S1 Paralel', 'angkatan': 2016, 'nm_status': 'Aktif', 'kd_status': '1'}, {'url': 'https://api.cs.ui.ac.id/siakngcs/program/62634/', 'periode': {'url': 'https://api.cs.ui.ac.id/siakngcs/periode/32/', 'term': 2, 'tahun': 2016}, 'kd_org': '08.00.12.01', 'nm_org': 'Sistem Informasi', 'nm_prg': 'S1 Paralel', 'angkatan': 2016, 'nm_status': 'Aktif', 'kd_status': '1'}, {'url': 'https://api.cs.ui.ac.id/siakngcs/program/60659/', 'periode': {'url': 'https://api.cs.ui.ac.id/siakngcs/periode/31/', 'term': 1, 'tahun': 2016}, 'kd_org': '08.00.12.01', 'nm_org': 'Sistem Informasi', 'nm_prg': 'S1 Paralel', 'angkatan': 2016, 'nm_status': 'Aktif', 'kd_status': '1'}]}
        extracted_data = extract_alumni_data(mhs_data)
        self.assertEqual(type(extracted_data), tuple)
        self.assertEqual(extracted_data[0], 'Wisnu Pramadhitya Ramadhan')
        self.assertEqual(extracted_data[1], '1606918055')
        self.assertEqual(extracted_data[2], '1998-01-14')
        self.assertEqual(extracted_data[3], 'S1-SI')
        self.assertEqual(extracted_data[4], 2016)

        user_data = {
            "email": "wisnu.rrr@gmail.com",
            "first_name": "wisnu",
            "last_name": "pramadhitya",
            "ui_sso_npm": "1606918055"
        }

        profile_data = {
            "birthdate": "1998-01-14",
            "latest_csui_program": "S1-IK",
            "latest_csui_class_year": 2016,
        }

        user = User.objects.create(**user_data)
        for k in profile_data.keys():
            setattr(user.profile, k, profile_data[k])
        user.profile.save()

        self.assertTrue(validate_alumni_data(user, *extracted_data))

    def test_extract_alumni_and_validate_without_npm(self):
        mhs_data = {'url': 'https://api.cs.ui.ac.id/siakngcs/mahasiswa/1606918055/', 'npm': '1606918055', 'nama': 'Wisnu Pramadhitya Ramadhan', 'alamat_mhs': 'Jl Amonia I Blok L-12 Kavling Pupuk Kujang', 'kd_pos_mhs': '16422', 'kota_lahir': 'Surabaya', 'tgl_lahir': '1998-01-14', 'program': [{'url': 'https://api.cs.ui.ac.id/siakngcs/program/1751028/', 'periode': {'url': 'https://api.cs.ui.ac.id/siakngcs/periode/38/', 'term': 2, 'tahun': 2018}, 'kd_org': '08.00.12.01', 'nm_org': 'Sistem Informasi', 'nm_prg': 'S1 Paralel', 'angkatan': 2016, 'nm_status': 'Aktif', 'kd_status': '1'}, {'url': 'https://api.cs.ui.ac.id/siakngcs/program/1748930/', 'periode': {'url': 'https://api.cs.ui.ac.id/siakngcs/periode/37/', 'term': 1, 'tahun': 2018}, 'kd_org': '08.00.12.01', 'nm_org': 'Sistem Informasi', 'nm_prg': 'S1 Paralel', 'angkatan': 2016, 'nm_status': 'Aktif', 'kd_status': '1'}, {'url': 'https://api.cs.ui.ac.id/siakngcs/program/1270974/', 'periode': {'url': 'https://api.cs.ui.ac.id/siakngcs/periode/36/', 'term': 3, 'tahun': 2017}, 'kd_org': '08.00.12.01', 'nm_org': 'Sistem Informasi', 'nm_prg': 'S1 Paralel', 'angkatan': 2016, 'nm_status': 'Kosong', 'kd_status': '0'}, {'url': 'https://api.cs.ui.ac.id/siakngcs/program/1269703/', 'periode': {
            'url': 'https://api.cs.ui.ac.id/siakngcs/periode/35/', 'term': 2, 'tahun': 2017}, 'kd_org': '08.00.12.01', 'nm_org': 'Sistem Informasi', 'nm_prg': 'S1 Paralel', 'angkatan': 2016, 'nm_status': 'Aktif', 'kd_status': '1'}, {'url': 'https://api.cs.ui.ac.id/siakngcs/program/1267681/', 'periode': {'url': 'https://api.cs.ui.ac.id/siakngcs/periode/34/', 'term': 1, 'tahun': 2017}, 'kd_org': '08.00.12.01', 'nm_org': 'Sistem Informasi', 'nm_prg': 'S1 Paralel', 'angkatan': 2016, 'nm_status': 'Aktif', 'kd_status': '1'}, {'url': 'https://api.cs.ui.ac.id/siakngcs/program/45168/', 'periode': {'url': 'https://api.cs.ui.ac.id/siakngcs/periode/33/', 'term': 3, 'tahun': 2016}, 'kd_org': '08.00.12.01', 'nm_org': 'Sistem Informasi', 'nm_prg': 'S1 Paralel', 'angkatan': 2016, 'nm_status': 'Aktif', 'kd_status': '1'}, {'url': 'https://api.cs.ui.ac.id/siakngcs/program/62634/', 'periode': {'url': 'https://api.cs.ui.ac.id/siakngcs/periode/32/', 'term': 2, 'tahun': 2016}, 'kd_org': '08.00.12.01', 'nm_org': 'Sistem Informasi', 'nm_prg': 'S1 Paralel', 'angkatan': 2016, 'nm_status': 'Aktif', 'kd_status': '1'}, {'url': 'https://api.cs.ui.ac.id/siakngcs/program/60659/', 'periode': {'url': 'https://api.cs.ui.ac.id/siakngcs/periode/31/', 'term': 1, 'tahun': 2016}, 'kd_org': '08.00.12.01', 'nm_org': 'Sistem Informasi', 'nm_prg': 'S1 Paralel', 'angkatan': 2016, 'nm_status': 'Aktif', 'kd_status': '1'}]}
        extracted_data = extract_alumni_data(mhs_data)
        self.assertEqual(type(extracted_data), tuple)
        self.assertEqual(extracted_data[0], 'Wisnu Pramadhitya Ramadhan')
        self.assertEqual(extracted_data[1], '1606918055')
        self.assertEqual(extracted_data[2], '1998-01-14')
        self.assertEqual(extracted_data[3], 'S1-SI')
        self.assertEqual(extracted_data[4], 2016)

        user_data = {
            "email": "wisnu.rrr@gmail.com",
            "first_name": "wisnu",
            "last_name": "pramadhitya",
        }

        profile_data = {
            "birthdate": "1998-01-14",
            "latest_csui_program": "S1-IK",
            "latest_csui_class_year": 2016,
        }

        user = User.objects.create(**user_data)
        for k in profile_data.keys():
            setattr(user.profile, k, profile_data[k])
        user.profile.save()

        # salah di IK ngurang 20 point terus ga pake NPM
        self.assertFalse(validate_alumni_data(user, *extracted_data))

    def test_extract_alumni_and_validate_without_npm_passed(self):
        mhs_data = {'url': 'https://api.cs.ui.ac.id/siakngcs/mahasiswa/1606918055/', 'npm': '1606918055', 'nama': 'Wisnu Pramadhitya Ramadhan', 'alamat_mhs': 'Jl Amonia I Blok L-12 Kavling Pupuk Kujang', 'kd_pos_mhs': '16422', 'kota_lahir': 'Surabaya', 'tgl_lahir': '1998-01-14', 'program': [{'url': 'https://api.cs.ui.ac.id/siakngcs/program/1751028/', 'periode': {'url': 'https://api.cs.ui.ac.id/siakngcs/periode/38/', 'term': 2, 'tahun': 2018}, 'kd_org': '08.00.12.01', 'nm_org': 'Sistem Informasi', 'nm_prg': 'S1 Paralel', 'angkatan': 2016, 'nm_status': 'Aktif', 'kd_status': '1'}, {'url': 'https://api.cs.ui.ac.id/siakngcs/program/1748930/', 'periode': {'url': 'https://api.cs.ui.ac.id/siakngcs/periode/37/', 'term': 1, 'tahun': 2018}, 'kd_org': '08.00.12.01', 'nm_org': 'Sistem Informasi', 'nm_prg': 'S1 Paralel', 'angkatan': 2016, 'nm_status': 'Aktif', 'kd_status': '1'}, {'url': 'https://api.cs.ui.ac.id/siakngcs/program/1270974/', 'periode': {'url': 'https://api.cs.ui.ac.id/siakngcs/periode/36/', 'term': 3, 'tahun': 2017}, 'kd_org': '08.00.12.01', 'nm_org': 'Sistem Informasi', 'nm_prg': 'S1 Paralel', 'angkatan': 2016, 'nm_status': 'Kosong', 'kd_status': '0'}, {'url': 'https://api.cs.ui.ac.id/siakngcs/program/1269703/', 'periode': {
            'url': 'https://api.cs.ui.ac.id/siakngcs/periode/35/', 'term': 2, 'tahun': 2017}, 'kd_org': '08.00.12.01', 'nm_org': 'Sistem Informasi', 'nm_prg': 'S1 Paralel', 'angkatan': 2016, 'nm_status': 'Aktif', 'kd_status': '1'}, {'url': 'https://api.cs.ui.ac.id/siakngcs/program/1267681/', 'periode': {'url': 'https://api.cs.ui.ac.id/siakngcs/periode/34/', 'term': 1, 'tahun': 2017}, 'kd_org': '08.00.12.01', 'nm_org': 'Sistem Informasi', 'nm_prg': 'S1 Paralel', 'angkatan': 2016, 'nm_status': 'Aktif', 'kd_status': '1'}, {'url': 'https://api.cs.ui.ac.id/siakngcs/program/45168/', 'periode': {'url': 'https://api.cs.ui.ac.id/siakngcs/periode/33/', 'term': 3, 'tahun': 2016}, 'kd_org': '08.00.12.01', 'nm_org': 'Sistem Informasi', 'nm_prg': 'S1 Paralel', 'angkatan': 2016, 'nm_status': 'Aktif', 'kd_status': '1'}, {'url': 'https://api.cs.ui.ac.id/siakngcs/program/62634/', 'periode': {'url': 'https://api.cs.ui.ac.id/siakngcs/periode/32/', 'term': 2, 'tahun': 2016}, 'kd_org': '08.00.12.01', 'nm_org': 'Sistem Informasi', 'nm_prg': 'S1 Paralel', 'angkatan': 2016, 'nm_status': 'Aktif', 'kd_status': '1'}, {'url': 'https://api.cs.ui.ac.id/siakngcs/program/60659/', 'periode': {'url': 'https://api.cs.ui.ac.id/siakngcs/periode/31/', 'term': 1, 'tahun': 2016}, 'kd_org': '08.00.12.01', 'nm_org': 'Sistem Informasi', 'nm_prg': 'S1 Paralel', 'angkatan': 2016, 'nm_status': 'Aktif', 'kd_status': '1'}]}
        extracted_data = extract_alumni_data(mhs_data)
        self.assertEqual(type(extracted_data), tuple)
        self.assertEqual(extracted_data[0], 'Wisnu Pramadhitya Ramadhan')
        self.assertEqual(extracted_data[1], '1606918055')
        self.assertEqual(extracted_data[2], '1998-01-14')
        self.assertEqual(extracted_data[3], 'S1-SI')
        self.assertEqual(extracted_data[4], 2016)

        user_data = {
            "email": "wisnu.rrr@gmail.com",
            "first_name": "wisnu",
            "last_name": "pramadhitya",
        }

        profile_data = {
            "birthdate": "1998-01-14",
            "latest_csui_program": "S1-SI",
            "latest_csui_class_year": 2016,
        }

        user = User.objects.create(**user_data)
        for k in profile_data.keys():
            setattr(user.profile, k, profile_data[k])
        user.profile.save()

        self.assertTrue(validate_alumni_data(user, *extracted_data))
