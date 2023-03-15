from django.db import models
from django.contrib.auth import get_user_model

JAWABAN_SINGKAT = 'Jawaban Singkat'
JENIS_PERTANYAAN = [
    (JAWABAN_SINGKAT, JAWABAN_SINGKAT),
    ('Paragraf', 'Paragraf'),
    ('Pilihan Ganda', 'Pilihan Ganda'),
    ('Kotak Centang', 'Kotak Centang'),
    ('Drop-Down', 'Drop-Down'),
    ('Skala Linear', 'Skala Linear'),
    ('Tanggal', 'Tanggal'),
    ('Waktu', 'Waktu')
]

User = get_user_model()


class Survei(models.Model):
    nama = models.CharField(max_length=150)
    deskripsi = models.CharField(max_length=1200)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    tanggal_dikirim = models.DateTimeField(null=True, blank=True)
    sudah_dikirim = models.BooleanField(default=False)
    tanggal_dibuat = models.DateTimeField(auto_now_add=True)
    tanggal_diedit = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.nama


class Pertanyaan(models.Model):
    survei = models.ForeignKey(Survei, on_delete=models.CASCADE)
    pertanyaan = models.CharField(max_length=1200)
    jenis_jawaban = models.CharField(
        choices=JENIS_PERTANYAAN,
        default=JAWABAN_SINGKAT,
        max_length=50
    )
    wajib_diisi = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{str(self.survei)} - {self.pertanyaan}"


class OpsiJawaban(models.Model):
    pertanyaan = models.ForeignKey(Pertanyaan, on_delete=models.CASCADE)
    opsi_jawaban = models.CharField(max_length=150)

    def __str__(self) -> str:
        return f"{str(self.pertanyaan)} - {self.opsi_jawaban}"
