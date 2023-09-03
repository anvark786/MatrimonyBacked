# Generated by Django 4.2.2 on 2023-08-13 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_remove_profile_religion_profile_community'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='name',
            field=models.CharField(choices=[('sslc', 'SSLC'), ('pls_two', 'Plus Two'), ('degree', 'Bachelor Degree'), ('pg', 'Master Degree')], max_length=15),
        ),
        migrations.AlterField(
            model_name='occupation',
            name='profession',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='occupation',
            name='profession_type',
            field=models.CharField(max_length=100),
        ),
    ]