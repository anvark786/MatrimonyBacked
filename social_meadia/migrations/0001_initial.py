# Generated by Django 4.2.2 on 2023-09-03 18:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0013_rename_is_locked_profile_is_locked_photos_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(choices=[('Facebook', 'Facebook'), ('Twitter', 'Twitter'), ('LinkedIn', 'LinkedIn'), ('Instagram', 'Instagram'), ('YouTube', 'YouTube'), ('GitHub', 'GitHub'), ('WhatsApp', 'WhatsApp')], max_length=20)),
                ('url', models.URLField()),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='creator_%(class)s_objects', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_media', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='updator_%(class)s_objects', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Social_meadia',
                'verbose_name_plural': 'Social_meadias',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SocialLinkAccessRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('declined ', 'Declined ')], default='pending', max_length=10)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='creator_%(class)s_objects', to=settings.AUTH_USER_MODEL)),
                ('profile_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_social_link_access_requests_received', to='profiles.profile')),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_social_link_access_requests_made', to='profiles.profile')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='updator_%(class)s_objects', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Social_link_access_request',
                'verbose_name_plural': 'Social_link_access_requests',
                'ordering': ['-created_at'],
                'unique_together': {('requester', 'profile_owner')},
            },
        ),
    ]
