from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('provider', 'Provider'),
        ('both', 'Both'),
        ('none', 'None'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='none')
    
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.username

    @property
    def is_customer(self):
        return self.role in ['customer', 'both']

    @property
    def is_provider(self):
        return self.role in ['provider', 'both']

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True, help_text="Short bio for service providers")
    location = models.CharField(max_length=100, blank=True, help_text="City or Area")
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Ensure profile exists before saving
    profile, created = Profile.objects.get_or_create(user=instance)
    profile.save()
