# Generated by Django 2.1.7 on 2019-04-07 20:19

import atlas.apps.account.managers
from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0010_merge_20190405_1352'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('account.user',),
            managers=[
                ('objects', atlas.apps.account.managers.UserManager()),
            ],
        ),
    ]
