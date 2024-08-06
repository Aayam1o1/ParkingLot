import factory
from factory.django import DjangoModelFactory
from factory import Faker, SubFactory
from rest_api.models import Parking, CustomUser, VehicleDetail, VehicleOwner, ParkingDetail

class CustomUserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser
        skip_postgeneration_save = True
   
    email = Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'password')
    is_staff = False
    is_superuser = False
    is_employee = False
    is_owner = False
    is_active = True
    


class ParkingFactory(DjangoModelFactory):
    class Meta:
        model = Parking
        skip_postgeneration_save = True

    wing_name = Faker('word')
    is_available = True
    
    

    
class VehicleDetailFactory(DjangoModelFactory):
    class Meta:
        model = VehicleDetail
        skip_postgeneration_save = True

    vehicle_number = Faker('license_plate')
    vehicle_type = Faker('word')
    vehicle_brand = Faker('word')
    
    
class VehicleOwnerFactory(DjangoModelFactory):
    class Meta:
        model = VehicleOwner
        skip_postgeneration_save = True
        
    user = SubFactory(CustomUserFactory)  
    name = Faker('name')
    phone_number = Faker('phone_number')
    address = Faker('address')
    owned_vehicle = SubFactory(VehicleDetailFactory)


class ParkingDetailFactory(DjangoModelFactory):
    class Meta:
        model = ParkingDetail
        skip_postgeneration_save = True

    parking_wing = factory.SubFactory(ParkingFactory)
    vehicle_arrived_date = factory.Faker('date')
    vehicle_arrived_time = factory.Faker('time')
    vehicle_left_date = factory.Faker('date')
    vehicle_left_time = factory.Faker('time')
    vehicle_has_left = False

    @factory.post_generation
    def vehicles(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for vehicle in extracted:
                self.vehicles.add(vehicle)