from django.db import models
from datetime import datetime


# Create your models here.
class Parking(models.Model):
    wingName = models.CharField(max_length=30, unique=True)
    isAvailable = models.BooleanField(default=True)
    
    def __str__(self):
            return self.wingName
        
class CarDetail(models.Model):
    vehicleNumber = models.CharField(max_length=30)
    ownerName = models.CharField(max_length=30)
    phoneNumber = models.CharField(max_length=10)
    vehicleType = models.CharField(max_length=30)
    date = models.DateTimeField(default=datetime.now)
    parkingWing = models.ForeignKey(Parking, on_delete=models.CASCADE, blank=True)
    
    def __str__(self):
        return self.vehicleNumber
    

    