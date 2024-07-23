from django.contrib import admin
from rest_api.models import (
    CustomUser,
    Parking,
    ParkingDetail,
    VehicleDetail,
    VehicleOwner,
)

# Register your models here.
admin.site.register(Parking),
admin.site.register(VehicleDetail),
admin.site.register(ParkingDetail),
admin.site.register(CustomUser),
admin.site.register(VehicleOwner)
