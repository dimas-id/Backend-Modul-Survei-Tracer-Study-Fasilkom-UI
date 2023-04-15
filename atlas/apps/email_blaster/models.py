from django.db import models


class EmailTemplate(models.Model):
    title = models.CharField(max_length=150)
    email_subject = models.CharField(max_length=150)
    email_body = models.TextField()

    def __str__(self):
        return f"{self.title} - {self.email_subject}"
