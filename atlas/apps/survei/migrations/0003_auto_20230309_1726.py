# Generated by Django 2.1.7 on 2023-03-09 10:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('survei', '0002_auto_20230309_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='survei',
            name='tanggal_dibuat',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='survei',
            name='tanggal_diedit',
            field=models.DateTimeField(auto_created=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
