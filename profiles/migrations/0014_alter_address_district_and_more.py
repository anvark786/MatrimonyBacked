# Generated by Django 4.2.2 on 2024-07-03 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0013_rename_is_locked_profile_is_locked_photos_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='district',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='preference',
            name='preferred_district',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
