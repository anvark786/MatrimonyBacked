
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]    

    phone_number = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True) 
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']