from django.db import models
from users.models import User
from matrimony.models import BaseModel
from profiles.models import Profile


class SocialMedia(BaseModel):
    SOCIAL_MEDIA_CHOICES = (
        ('Facebook', 'Facebook'),
        ('Twitter', 'Twitter'),
        ('LinkedIn', 'LinkedIn'),
        ('Instagram', 'Instagram'),
        ('YouTube', 'YouTube'),
        ('GitHub', 'GitHub'),
        ('WhatsApp', 'WhatsApp')
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_media')
    name = models.CharField(max_length=20, choices=SOCIAL_MEDIA_CHOICES)
    url = models.URLField()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Social_meadia'
        verbose_name_plural = 'Social_meadias'
        ordering = ['-created_at']

class SocialLinkAccessRequest(BaseModel):
    requester = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_social_link_access_requests_made')
    profile_owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_social_link_access_requests_received')
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('declined ', 'Declined ')], default='pending')  

    def __str__(self):
        f"AccessRequest send {self.requester.user.username} to {self.profile_owner.user.username}"
    
    class Meta:
        unique_together = ('requester', 'profile_owner')
        verbose_name = 'Social_link_access_request'
        verbose_name_plural = 'Social_link_access_requests'
        ordering = ['-created_at']

