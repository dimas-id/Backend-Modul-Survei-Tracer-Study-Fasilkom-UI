from atlas.apps.survei.models import OpsiJawaban, Pertanyaan, Survei
from django.db import (transaction)
from django.contrib.auth import get_user_model

class SurveiService:
    @transaction.atomic
    def register_suvei(self, request, nama, deskripsi, tanggal_dikirim=None, sudah_dikirim=False):
        user_model = get_user_model()

        try:
            user = user_model.objects.get(email=request.user)
            survei = Survei.objects.create(
                nama=nama, deskripsi=deskripsi, creator=user, tanggal_dikirim=tanggal_dikirim, sudah_dikirim=sudah_dikirim)
            return survei
        except user_model.DoesNotExist:
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
    def list_survei_sent(self):
        return Survei.objects.filter(sudah_dikirim=True)

    @transaction.atomic
    def list_survei_not_sent(self):
        return Survei.objects.filter(sudah_dikirim=False)

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