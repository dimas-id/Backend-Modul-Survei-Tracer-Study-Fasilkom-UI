# Generated by Django 2.1.7 on 2019-04-05 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('external_auth', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='linkedinaccount',
            name='api_standard_profile_request',
        ),
        migrations.RemoveField(
            model_name='linkedinaccount',
            name='public_profile_url',
        ),
    ]
