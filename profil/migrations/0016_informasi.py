# Generated by Django 2.2.19 on 2021-07-20 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profil', '0015_sdm'),
    ]

    operations = [
        migrations.CreateModel(
            name='informasi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.PositiveIntegerField(blank=True, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('link', models.CharField(blank=True, max_length=255, null=True)),
                ('facebook', models.CharField(blank=True, max_length=100, null=True)),
                ('instagram', models.CharField(blank=True, max_length=100, null=True)),
                ('twiter', models.CharField(blank=True, max_length=100, null=True)),
                ('whatsapp', models.CharField(blank=True, max_length=100, null=True)),
                ('youtube', models.CharField(blank=True, max_length=100, null=True)),
                ('tanggal', models.DateField(auto_now=True)),
            ],
        ),
    ]
