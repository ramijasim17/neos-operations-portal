"""Auto-create a Profile for every new User, so code can always safely
assume request.user.profile exists without a None-check everywhere."""

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_save_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        # If a Profile is somehow missing (e.g. a user created before this
        # app existed), create it rather than raising an error.
        Profile.objects.get_or_create(user=instance)
