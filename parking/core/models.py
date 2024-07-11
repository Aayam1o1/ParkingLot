from django.db import models
from django.utils import timezone
from django.utils import timezone

# Create your models here.
class Parking(models.Model):
    """"
    This model is created for storing Parking Wing information\
    
    Stores wing name and information about if the wing is available or not for
    parking purposes.
    """
    
    wing_name = models.CharField(max_length=30, unique=True)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
            return self.wing_name
        
class CarDetail(models.Model):
    """
    This model is created for storing the car details and information about the 
    owner of the car.
    
    Stores vehicle number, type and owner's name number. 
    """
    
    
    vehicle_number = models.CharField(max_length=30)
    owner = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=10)
    vehicle_type = models.CharField(max_length=30)
    date = models.DateTimeField(default=timezone.now)
    parking_wing = models.ForeignKey(Parking, on_delete=models.CASCADE, blank=True)
    
    def __str__(self):
        return self.vehicle_number
    
    
class ParkingDetail(models.Model):
    """
    This model is used to store information about details regarding the vehicle parking.
    
    This model saves the vehicle number and wing to get information about parked location of specific 
    vehicle, also storing the data of entry of vehicle and which time the vehicle left.
     
    """
    vehicle_arrived_date = models.DateField(default=timezone.now)
    vehicle_arrived_time = models.TimeField(default=timezone.now)
    vehicle_number = models.ForeignKey(CarDetail, on_delete=models.CASCADE, blank=True)
    parking_wing = models.ForeignKey(Parking, on_delete=models.CASCADE, blank=True)
    vehicle_left_date = models.DateField(blank = True, null=True)
    vehicle_left_time = models.TimeField(blank=True, null=True)
    vehicle_has_left = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.vehicle_number)
    
    
class OwnerProfile(models.Model):
    owned_car = models.OneToOneField(CarDetail, on_delete=models.CASCADE, blank = True, null = True)
    number_profile = models.CharField(max_length=30)
    vehicle_number_profile = models.CharField(max_length=30)
    vehicle_type_profile = models.CharField(max_length=30)
    owner_address = models.CharField(max_length=30, blank = True, null = True)
    owner_gender = models.CharField(max_length=30, blank = True, null = True)
    
    def __str__(self):
        return str(self.vehicle_number_profile)
    
    
