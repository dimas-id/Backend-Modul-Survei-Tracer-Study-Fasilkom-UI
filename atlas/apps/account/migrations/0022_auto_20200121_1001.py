# Generated by Django 2.1.7 on 2020-01-21 03:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0021_auto_20200107_1344'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='latest_csui_class_year',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='latest_csui_graduation_status',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='latest_csui_program',
        ),
    ]
