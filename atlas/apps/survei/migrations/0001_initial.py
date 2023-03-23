# Generated by Django 2.1.7 on 2023-03-09 06:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OpsiJawaban',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opsi_jawaban', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Pertanyaan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pertanyaan', models.TextField()),
                ('wajib_diisi', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Survei',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=150)),
                ('tanggal_dikirim', models.DateTimeField()),
                ('sudah_dikirim', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='pertanyaan',
            name='survei',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survei.Survei'),
        ),
        migrations.AddField(
            model_name='opsijawaban',
            name='pertanyaan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survei.Pertanyaan'),
        ),
    ]