# Generated by Django 4.2.2 on 2023-08-13 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_profile_profile_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_id',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]
