# Generated by Django 4.2.2 on 2024-07-07 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_tempuser_options_alter_user_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tempuser',
            name='is_verified_phone_number',
            field=models.BooleanField(default=False),
        ),
    ]