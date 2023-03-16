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
    def list_survei_sent(self):
        return Survei.objects.filter(sudah_dikirim=True)

    @transaction.atomic
    def list_survei_not_sent(self):
        return Survei.objects.filter(sudah_dikirim=False)
