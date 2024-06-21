from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta

# Create your models here.
class Profile(models.Model):
    rank_choices = [
        ('Bronze', 'Bronze'),
        ('Silver', 'Silver'),
        ('Gold', 'Gold'),
        ('Platinum', 'Platinum'),
        ('Diamond', 'Diamond'),
        ('Master', 'Master'),
        ('Predator', 'Predator'),
    ]

    type_choices = [
        ('PS4/PS5', 'PS4/PS5'),
        ('XBOX', 'XBOX'),
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
    type = models.CharField(max_length=100, choices=type_choices)
    rank = models.CharField(max_length=100, choices=rank_choices)
    gaming_id = models.CharField(max_length=100, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', default='default-thumbnail.jpg')
    last_active = models.DateTimeField(null=True, blank=True)

    

    def __str__(self):
        return self.user.email