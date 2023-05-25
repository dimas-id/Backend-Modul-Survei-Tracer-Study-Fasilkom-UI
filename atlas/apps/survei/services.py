import datetime
from atlas.apps.survei.models import OpsiJawaban, Pertanyaan, Survei
from django.db import (transaction)
from django.contrib.auth import get_user_model


class SurveiService:
    DELETE_SUCCESS = 0
    DELETE_NOT_FOUND = 1
    DELETE_PUBLISHED = 2

    @transaction.atomic
    def register_survei(self, request, nama, deskripsi, tanggal_dikirim=None, sudah_dikirim=False, sudah_final=False):
        user_model = get_user_model()

        try:
            user = user_model.objects.get(email=request.user)
            survei = Survei.objects.create(
                nama=nama, deskripsi=deskripsi, creator=user, tanggal_dikirim=tanggal_dikirim, sudah_dikirim=sudah_dikirim, sudah_final=sudah_final)
            return survei
        except user_model.DoesNotExist:
            return None

    @transaction.atomic
    def finalize(self, id):
        try:
            survei = Survei.objects.get(id=id)
            if (survei.sudah_final):
                return False
            survei.sudah_final = True
            survei.save()
            return survei.sudah_final
        except Survei.DoesNotExist:
            return None

    @transaction.atomic
    def list_survei(self):
        return Survei.objects.all()

    @transaction.atomic
    def get_survei(self, survei_id):
        try:
            survei = Survei.objects.get(id=survei_id)
            return survei
        except Survei.DoesNotExist:
            return None

    @transaction.atomic
    def get_list_pertanyaan_by_survei_id(self, s_id):
        return Pertanyaan.objects.filter(survei_id=s_id)

    @transaction.atomic
    def get_list_opsi_jawaban(self, s_id):
        list_pertanyaan = self.get_list_pertanyaan_by_survei_id(s_id)
        list_id_pertanyaan = []
        for pertanyaan in list_pertanyaan:
            list_id_pertanyaan.append(pertanyaan.id)
        return OpsiJawaban.objects.filter(pertanyaan_id__in=list_id_pertanyaan)

    @transaction.atomic
    def list_survei_sent(self):
        return Survei.objects.filter(sudah_final=True, sudah_dikirim=True).order_by('-tanggal_dikirim')

    @transaction.atomic
    def list_survei_not_sent(self):
        return Survei.objects.filter(sudah_dikirim=False)

    @transaction.atomic
    def list_survei_draft(self):
        return Survei.objects.filter(sudah_final=False, sudah_dikirim=False).order_by('-tanggal_diedit')

    @transaction.atomic
    def list_survei_finalized(self):
        return Survei.objects.filter(sudah_final=True, sudah_dikirim=False).order_by('-tanggal_diedit')

    @transaction.atomic
    def register_pertanyaan_isian(self, survei, pertanyaan, wajib_diisi=False):
        pertanyaan = Pertanyaan.objects.create(
            survei=survei,
            pertanyaan=pertanyaan,
            jenis_jawaban="Jawaban Singkat",
            wajib_diisi=wajib_diisi)
        return pertanyaan

    @transaction.atomic
    def register_opsi_jawaban_isian(self, pertanyaan, isian):
        try:
            jawaban_isian = OpsiJawaban.objects.create(
                pertanyaan=pertanyaan, opsi_jawaban=isian)
            return jawaban_isian
        except:
            return None

    @transaction.atomic
    def register_pertanyaan_skala_linier(self, survei, pertanyaan, wajib_diisi=False):
        pertanyaan = Pertanyaan.objects.create(
            survei=survei,
            pertanyaan=pertanyaan,
            jenis_jawaban="Skala Linear",
            wajib_diisi=wajib_diisi)
        return pertanyaan

    @transaction.atomic
    def register_opsi_jawaban_skala_linier(self, pertanyaan, skala):
        skala_linier = OpsiJawaban.objects.create(
            pertanyaan=pertanyaan, opsi_jawaban=skala)
        return skala_linier

    @transaction.atomic
    def register_pertanyaan_radiobutton(self, survei, pertanyaan, wajib_diisi=False):
        pertanyaan = Pertanyaan.objects.create(
            survei=survei,
            pertanyaan=pertanyaan,
            jenis_jawaban="Pilihan Ganda",
            wajib_diisi=wajib_diisi)
        return pertanyaan

    @transaction.atomic
    def register_opsi_jawaban_radiobutton(self, pertanyaan, pilihan_jawaban):
        opsi_jawaban_obj = OpsiJawaban.objects.create(
            pertanyaan=pertanyaan,
            opsi_jawaban=pilihan_jawaban)
        return opsi_jawaban_obj

    @transaction.atomic
    def register_pertanyaan_dropdown(self, survei, pertanyaan, wajib_diisi=False):
        pertanyaan = Pertanyaan.objects.create(
            survei=survei,
            pertanyaan=pertanyaan,
            jenis_jawaban="Drop-Down",
            wajib_diisi=wajib_diisi)
        return pertanyaan

    @transaction.atomic
    def register_opsi_jawaban_dropdown(self, pertanyaan, pilihan_jawaban):
        opsi_jawaban_obj = OpsiJawaban.objects.create(
            pertanyaan=pertanyaan,
            opsi_jawaban=pilihan_jawaban)
        return opsi_jawaban_obj

    @transaction.atomic
    def register_pertanyaan_checkbox(self, survei, pertanyaan, wajib_diisi=False):
        pertanyaan = Pertanyaan.objects.create(
            survei=survei,
            pertanyaan=pertanyaan,
            jenis_jawaban="Kotak Centang",
            wajib_diisi=wajib_diisi)
        return pertanyaan

    @transaction.atomic
    def register_opsi_jawaban_checkbox(self, pertanyaan, pilihan_jawaban):
        opsi_jawaban_obj = OpsiJawaban.objects.create(
            pertanyaan=pertanyaan,
            opsi_jawaban=pilihan_jawaban)
        return opsi_jawaban_obj

    @transaction.atomic
    def delete_survei(self, survei_id):
        '''
        Return `(status, value)`:\n
        - `status` bernilai 0 jika success; 1 jika not-found
        - `value` bernilai return value fungsi `delete()` Django
        '''
        delete_status = self.DELETE_NOT_FOUND
        delete_value = None
        try:
            survei = Survei.objects.get(id=survei_id)
            if survei.sudah_dikirim == True:
                delete_status = self.DELETE_PUBLISHED
            else:
                delete_value = survei.delete()
                delete_status = self.DELETE_SUCCESS
        except Survei.DoesNotExist:
            delete_status = self.DELETE_NOT_FOUND
        return (delete_status, delete_value)

    @transaction.atomic
    def delete_all_pertanyaan_by_survei_id(self, survei_id):
        '''
        Return `(status, value)`:\n
        - `status` bernilai 0 jika success; 1 jika not-found
        - `value` bernilai return value fungsi `delete()` Django
        '''
        delete_status = self.DELETE_NOT_FOUND
        delete_value = None
        try:
            pertanyaan = Pertanyaan.objects.filter(survei_id=survei_id)
            delete_value = pertanyaan.delete()
            delete_status = self.DELETE_SUCCESS
        except Pertanyaan.DoesNotExist:
            delete_status = self.DELETE_NOT_FOUND
        return (delete_status, delete_value)

    @transaction.atomic
    def set_kirim(self, survei_id):
        if Survei.objects.filter(id=survei_id).exists():
            survei = Survei.objects.get(id=survei_id)
            survei.sudah_dikirim = True
            survei.tanggal_dikirim = datetime.datetime.now()
            survei.save()
