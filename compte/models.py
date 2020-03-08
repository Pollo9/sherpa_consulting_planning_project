from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.dispatch import receiver
from django.db.models.signals import post_save

class profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	telephone = models.CharField(default=' ',max_length=400)
	adresse = models.CharField(default=' ',max_length=400)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()