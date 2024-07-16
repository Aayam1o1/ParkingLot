from django.contrib import admin
from rest_api.models import Parking, VehicleDetail, ParkingDetail


# Register your models here.
admin.site.register(Parking),
admin.site.register(VehicleDetail),
admin.site.register(ParkingDetail)