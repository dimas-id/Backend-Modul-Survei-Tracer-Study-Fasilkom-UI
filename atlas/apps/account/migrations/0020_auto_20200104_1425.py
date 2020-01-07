# Generated by Django 2.1.7 on 2020-01-04 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_auto_20190916_2346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='website_url',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='linkedin_url',
            field=models.URLField(blank=True, null=True, verbose_name='Linkedin URL'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='latest_csui_program',
            field=models.CharField(blank=True, choices=[('S1-IK', 'S1 - Ilmu Komputer'), ('S1_KI-IK', 'S1 KI - Ilmu Komputer'), ('S1-SI', 'S1 - Sistem Informasi'), ('S1_EKS-SI', 'S1 Ekstensi - Sistem Informasi'), ('S2-IK', 'S2 - Ilmu Komputer'), ('S2-TI', 'S2 - Teknologi Informasi'), ('S3-IK', 'S3 - Ilmu Komputer')], max_length=10, null=True, verbose_name='Prodi'),
        ),
    ]