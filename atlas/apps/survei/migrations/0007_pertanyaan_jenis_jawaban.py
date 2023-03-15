# Generated by Django 2.1.7 on 2023-03-14 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survei', '0006_survei_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='pertanyaan',
            name='jenis_jawaban',
            field=models.CharField(choices=[('Jawaban Singkat', 'Jawaban Singkat'), ('Paragraf', 'Paragraf'), ('Pilihan Ganda', 'Pilihan Ganda'), ('Kotak Centang', 'Kotak Centang'), ('Drop-Down', 'Drop-Down'), ('Skala Linear', 'Skala Linear'), ('Tanggal', 'Tanggal'), ('Waktu', 'Waktu')], default='Jawaban Singkat', max_length=50),
        ),
    ]
