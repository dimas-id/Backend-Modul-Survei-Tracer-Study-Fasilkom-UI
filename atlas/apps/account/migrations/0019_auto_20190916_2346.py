# Generated by Django 2.1.7 on 2019-09-16 16:46

import atlas.apps.account.utils
import atlas.libs.core.validators
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0018_auto_20190701_0356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(db_index=True, max_length=128, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, help_text="Designates that if this user is not active, then can't login.", verbose_name='Active status'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_email_verified',
            field=models.BooleanField(default=False, help_text="Designates that if this user email is not verified,then can't access other services except Account Service", verbose_name='Email Verified status'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates that this user can login to administrator site.', verbose_name='Staff status'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Menentukan apakah pengguna memiliki semua hak akses tanpa perlu diberikan secara manual.', verbose_name='Superuser status'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_verified',
            field=models.BooleanField(default=False, help_text="Designates that if this user is not verified,then can't access other services except Account Service", verbose_name='Verified status'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(db_index=True, max_length=128, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='preference',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=atlas.apps.account.utils.default_preference, help_text='Here is the user preference, we can add some later', verbose_name='User Preference'),
        ),
        migrations.AlterField(
            model_name='user',
            name='ui_sso_npm',
            field=models.CharField(blank=True, db_index=True, max_length=16, null=True, validators=[atlas.libs.core.validators.NumericRegex()], verbose_name='SSO UI NPM'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='birthdate',
            field=models.DateField(null=True, verbose_name='Birthdate'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True, verbose_name='Gender'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[atlas.libs.core.validators.PhoneRegex()], verbose_name='Phone Number'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic_url',
            field=models.URLField(blank=True, default='https://alumni-prod.s3-ap-southeast-1.amazonaws.com/img/default-profile-pic.jpeg', verbose_name='Profile Picture'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='residence_lat',
            field=models.FloatField(blank=True, null=True, verbose_name='Residence Latitude'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='residence_lng',
            field=models.FloatField(blank=True, null=True, verbose_name='Residence Longitude'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='website_url',
            field=models.URLField(blank=True, null=True, verbose_name='Website URL'),
        ),
    ]