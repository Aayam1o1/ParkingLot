from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin



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
    
    
    
    
class ParkingDetail(models.Model):
    parking_wing = models.ForeignKey(Parking, on_delete=models.CASCADE, blank=True)
    vehicles = models.ManyToManyField(VehicleDetail, blank=True, related_name="parking_details")
    vehicle_arrived_date = models.DateField(default=timezone.now)
    vehicle_arrived_time = models.TimeField(default=timezone.now)
    vehicle_left_date = models.DateField(blank = True, null=True)
    vehicle_left_time = models.TimeField(blank=True, null=True)
    vehicle_has_left = models.BooleanField(default=False)
    
    def __str__(self):
        vehicle_info = []
        for vehicle in self.vehicles.all():
            owner_name = vehicle.owner.name if vehicle.owner else "Unknown Owner"
            vehicle_info.append(f"{vehicle.vehicle_number} (Owner: {owner_name})")
        
        vehicle_details = ', '.join(vehicle_info)
        return f"Parking: {self.parking_wing}, Vehicles: {vehicle_details}"
    


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        print('44')
        if not email:
            raise ValueError('The Email field must be set')
        if not password:
            raise ValueError('The Password field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class AbstractCustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    class Meta:
        abstract = True


class CustomUser(AbstractCustomUser):
    is_employee = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    
    def __str__(self):
        return self.email

    
class VehicleOwner(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='vehicle_owner')

    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    owned_vehicle = models.OneToOneField(VehicleDetail, related_name='owner', on_delete=models.CASCADE, blank = True, null = True)
    
    
    def __str__(self):
        return self.name