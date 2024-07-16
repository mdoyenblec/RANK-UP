from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta

# Create your models here.
class Profile(models.Model):

    platform_choices = [
        ('PS4', 'PS4'),
        ('X1', 'XBOX'),
        ('PC', 'PC'),
    ]

    country_choices = [
        ('France', 'France'),
        ('Belgium', 'Belgium'),
        ('UK', 'UK'),
        ('Spain','Spain'),
        ('Germany','Germany'),
        ('Italy','Italy'),
        ('Greece','Greece'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    

    country = models.CharField(max_length=100, choices=country_choices)
    platform = models.CharField(max_length=100, choices=platform_choices)
    gaming_id = models.CharField(max_length=100, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', default='default-thumbnail.jpg')
    last_active = models.DateTimeField(null=True, blank=True)

    

    def __str__(self):
        return self.user.email