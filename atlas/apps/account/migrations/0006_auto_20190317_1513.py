# Generated by Django 2.1.7 on 2019-03-17 08:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_remove_user_preference'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='latest_csui_class',
            new_name='latest_csui_class_year',
        ),
    ]