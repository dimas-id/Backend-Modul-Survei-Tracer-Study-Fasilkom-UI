from django.db import models
from django.contrib.auth import get_user_model
from atlas.apps.survei.models import Survei, Pertanyaan

User = get_user_model()


class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    survei = models.ForeignKey(Survei, on_delete=models.CASCADE)
    tanggal_dibuat = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user} - {self.survei}"


class Jawaban(models.Model):
    pertanyaan = models.ForeignKey(Pertanyaan, on_delete=models.CASCADE)
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    jawaban = models.CharField(max_length=1200)
    tanggal_dibuat = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.response.user} - {self.pertanyaan} - {self.jawaban}"
