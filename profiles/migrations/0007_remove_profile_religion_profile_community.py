# Generated by Django 4.2.2 on 2023-08-13 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_remove_religion_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='religion',
        ),
        migrations.AddField(
            model_name='profile',
            name='community',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.community'),
        ),
    ]