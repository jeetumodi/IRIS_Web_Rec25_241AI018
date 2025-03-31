from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, OtherData

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

@receiver(post_save, sender=User)
def create_other_data(sender, instance, created, **kwargs):
    if created:  # Runs only when a new User is created
        OtherData.objects.create(user=instance, credits=0, CGPA=0.00, semester="N/A")