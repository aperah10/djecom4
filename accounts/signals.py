from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save, post_delete
from .models import *


# automatic profile
@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            uplod=instance,
            id=instance.id,
            fullname=instance.fullname,
            email=instance.email,
        )

