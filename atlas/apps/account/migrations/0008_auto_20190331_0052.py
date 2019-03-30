# Generated by Django 2.1.7 on 2019-03-30 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20190323_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='residence_lat',
            field=models.FloatField(blank=True, null=True, verbose_name='Residence Latitude'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='residence_lng',
            field=models.FloatField(blank=True, null=True, verbose_name='Residence Longitude'),
        ),
    ]
