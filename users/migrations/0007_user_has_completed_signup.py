# Generated by Django 4.2.2 on 2024-07-10 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_tempuser_is_verified_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='has_completed_signup',
            field=models.BooleanField(default=False),
        ),
    ]
