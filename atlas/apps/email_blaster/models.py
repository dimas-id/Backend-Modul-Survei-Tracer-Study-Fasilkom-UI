from django.db import models
from atlas.apps.survei.models import Survei


class EmailTemplate(models.Model):
    title = models.CharField(max_length=150)
    email_subject = models.CharField(max_length=150)
    email_body = models.TextField()

    def __str__(self):
        return f"{self.title} - {self.email_subject}"


class EmailRecipient(models.Model):
    survei = models.ForeignKey(Survei, on_delete=models.CASCADE)
    tanggal_dikirim = models.DateTimeField(auto_now_add=True)
    group_recipients_years = models.CharField(max_length=500)
    group_recipients_terms = models.CharField(max_length=500)
    individual_recipients_emails = models.CharField(max_length=1200)
    csv_emails = models.CharField(max_length=1200)

    def __str__(self) -> str:
        return f"{str(self.survei)} - {self.tanggal_dikirim}"