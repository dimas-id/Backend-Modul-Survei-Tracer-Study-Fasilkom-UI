# Generated by Django 2.1.7 on 2023-03-09 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survei', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='survei',
            name='deskripsi',
            field=models.CharField(default='keren', max_length=1200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pertanyaan',
            name='pertanyaan',
            field=models.CharField(max_length=1200),
        ),
    ]