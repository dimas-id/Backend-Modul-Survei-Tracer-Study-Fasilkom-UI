# Generated by Django 2.1.7 on 2019-03-08 16:03

import atlas.apps.account.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_preference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic_url',
            field=models.ImageField(blank=True, default='img/default-profile-pic.jpeg', upload_to=atlas.apps.account.utils.user_profile_pic_path, verbose_name='Profile Picture'),
        ),
    ]
