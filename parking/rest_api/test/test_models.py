from django.test import TestCase
from rest_api.models import Parking, VehicleDetail, ParkingDetail, VehicleOwner, CustomUser
from django.contrib.auth import get_user_model

class ParkingModelTest(TestCase):
    def setUp(self):
        self.parking = Parking.objects.create(wing_name='A', is_available=True)

    def test_parking_creation(self):
        self.assertEqual(self.parking.wing_name, 'A')
        self.assertTrue(self.parking.is_available)

class VehicleDetailModelTest(TestCase):
    def setUp(self):
        self.vehicle = VehicleDetail.objects.create(
            vehicle_number='ABC123',
            vehicle_type='Car',
            vehicle_brand='Toyota'
        )

    def test_vehicle_creation(self):
        self.assertEqual(self.vehicle.vehicle_number, 'ABC123')
        self.assertEqual(self.vehicle.vehicle_type, 'Car')
        self.assertEqual(self.vehicle.vehicle_brand, 'Toyota')

class ParkingDetailModelTest(TestCase):
    def setUp(self):
        self.parking = Parking.objects.create(wing_name='A', is_available=True)
        self.vehicle = VehicleDetail.objects.create(
            vehicle_number='ABC123',
            vehicle_type='Car',
            vehicle_brand='Toyota'
        )
        self.parking_detail = ParkingDetail.objects.create(parking_wing=self.parking)
        self.parking_detail.vehicles.add(self.vehicle)

    def test_parking_detail_creation(self):
        self.assertEqual(self.parking_detail.parking_wing, self.parking)
        self.assertIn(self.vehicle, self.parking_detail.vehicles.all())

class VehicleOwnerModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@example.com', password='password')
        self.vehicle = VehicleDetail.objects.create(
            vehicle_number='ABC123',
            vehicle_type='Car',
            vehicle_brand='Toyota'
        )
        self.owner = VehicleOwner.objects.create(
            user=self.user,
            name='John Doe',
            phone_number='1234567890',
            address='123 Main St',
            owned_vehicle=self.vehicle
        )

    def test_vehicle_owner_creation(self):
        self.assertEqual(self.owner.user, self.user)
        self.assertEqual(self.owner.name, 'John Doe')
        self.assertEqual(self.owner.phone_number, '1234567890')
        self.assertEqual(self.owner.address, '123 Main St')
        self.assertEqual(self.owner.owned_vehicle, self.vehicle)
        

class CustomUserTests(TestCase):

    def setUp(self):
        self.user_model = get_user_model()

    def test_create_user(self):
        email = 'testuser@example.com'
        password = 'password123'
        user = self.user_model.objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            self.user_model.objects.create_user(email='', password='password123')

    def test_create_user_without_password(self):
        with self.assertRaises(ValueError):
            self.user_model.objects.create_user(email='testuser@example.com', password='')

    def test_create_superuser(self):
        email = 'admin@example.com'
        password = 'password123'
        superuser = self.user_model.objects.create_superuser(email=email, password=password)
        self.assertEqual(superuser.email, email)
        self.assertTrue(superuser.check_password(password))
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_create_superuser_without_is_staff(self):
        with self.assertRaises(ValueError):
            self.user_model.objects.create_superuser(email='admin@example.com', password='password123', is_staff=False)

    def test_create_superuser_without_is_superuser(self):
        with self.assertRaises(ValueError):
            self.user_model.objects.create_superuser(email='admin@example.com', password='password123', is_superuser=False)

