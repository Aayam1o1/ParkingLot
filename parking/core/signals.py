from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CarDetail, OwnerProfile


@receiver(post_save, sender=CarDetail)
def create_owner_profile(sender, instance, created, **kwargs):
    """
    This signal is created when the car instance is created to automatically create owner profile
    """

    if created:
        OwnerProfile.objects.create(
            owned_car=instance,
            number_profile=instance.phone_number,
            vehicle_number_profile=instance.vehicle_number,
            vehicle_type_profile=instance.vehicle_type,
        )
