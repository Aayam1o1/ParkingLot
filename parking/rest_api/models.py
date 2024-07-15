from django.db import models
from django.utils import timezone
# Create your models here.
class Parking(models.Model):
    wing_name = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.wing_name
    
    
class VehicleDetail(models.Model):
    vehicle_number = models.CharField(max_length=255)
    vehicle_type = models.CharField(max_length=255)
    vehicle_brand = models.CharField(max_length=255)
    
    def __str__(self):
        return self.vehicle_number
    
    
class VehicleOwner(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    owned_vehicle = models.OneToOneField(VehicleDetail, on_delete=models.CASCADE, blank = True, null = True)
    
    
    def __str__(self):
        return self.name
    
    
class ParkingDetail(models.Model):
    parking_wing = models.ForeignKey(Parking, on_delete=models.CASCADE, blank=True)
    vehicles = models.ManyToManyField(VehicleDetail, blank=True, related_name="parking_details")
    vehicle_arrived_date = models.DateField(default=timezone.now)
    vehicle_arrived_time = models.TimeField(default=timezone.now)
    vehicle_left_date = models.DateField(blank = True, null=True)
    vehicle_left_time = models.TimeField(blank=True, null=True)
    vehicle_has_left = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.parking_wing + self.vehicles)