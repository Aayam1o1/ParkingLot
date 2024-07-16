# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from rest_api.models import VehicleOwner, VehicleDetail



# @receiver(post_save, sender=VehicleDetail)
# def create_owner_profile(sender, instance, created, extra_params=None, **kwargs):
#     print("🐍 File: rest_api/signals.py | Line: 9 | undefined ~ extra_param",extra_params)
#     print("🐍 File: rest_api/signals.py | Line: 9 | undefined ~ kwargs",kwargs)
#     """
#     Signal handler to create a VehicleOwner profile when a VehicleDetail is created.
#     """
#     if created:
#         print(instance.owner)
#         var = VehicleOwner.object.get(owned_vehicle = instance)
#         owner_data = {
#             'name': var.name,
#             'phone_number':var.phone_number,
#             'address': instance.owner['address']
            
#         }
#         VehicleOwner.objects.create(owned_vehicle=instance, **owner_data)