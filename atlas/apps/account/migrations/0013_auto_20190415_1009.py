# Generated by Django 2.1.7 on 2019-04-15 03:09

import atlas.libs.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_auto_20190411_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='ui_sso_npm',
            field=models.CharField(blank=True, max_length=16, null=True, validators=[atlas.libs.core.validators.NumericRegex()], verbose_name='SSO UI NPM'),
        ),
    ]
