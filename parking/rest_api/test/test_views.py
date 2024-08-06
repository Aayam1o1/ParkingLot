from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_api.models import CustomUser, Parking, ParkingDetail, VehicleDetail, VehicleOwner
from rest_api.serializers import ParkingSerializer
from rest_api.permissions import IsAdminUser, IsEmployee
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import datetime

#for Parking
class ParkingAPITests(APITestCase):
    def setUp(self):
        self.admin_user = self.create_user(email='admin@example.com', password='password', is_staff=True, is_superuser=True)
        self.employee_user = self.create_user(email='employee@example.com', password='password', is_employee=True)
        self.parking = Parking.objects.create(wing_name='A', is_available=True)
        self.owner_user = self.create_user(email='owner@example.com', password='password', is_owner=True)

    def create_user(self, email, password, is_staff=False, is_superuser=False, is_owner=False, is_employee=False):
        user = CustomUser.objects.create_user(email=email, password=password, is_staff=is_staff, is_superuser=is_superuser, is_owner=is_owner, is_employee=is_employee)
        return user

    def test_create_parking(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(reverse('rest_api:parking_create'), {'wing_name': 'B', 'is_available': False})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Parking.objects.count(), 2)

    def test_update_parking(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(reverse('rest_api:parking_update', kwargs={'pk': self.parking.id}), {'wing_name': 'C'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.parking.refresh_from_db()
        self.assertEqual(self.parking.wing_name, 'C')

    def test_list_parking(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(reverse('rest_api:parking_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  
      

    def test_retrieve_parking(self):
        self.client.force_authenticate(user=self.employee_user)
        response = self.client.get(reverse('rest_api:parking_retrive', kwargs={'pk': self.parking.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['wing_name'], 'A')

    def test_delete_parking(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(reverse('rest_api:parking_delete', kwargs={'pk': self.parking.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Parking.objects.count(), 0)
        
#for parking details
class ParkingDetailAPITests(APITestCase):

    def setUp(self):
        self.admin_user = self.create_user(email='admin@example.com', password='password', is_staff=True, is_superuser=True)
        self.employee_user = self.create_user(email='employee@example.com', password='password', is_staff=True, is_employee=True)
        self.owner_user = self.create_user(email='owner@example.com', password='password', is_staff=True, is_owner=True)
        
        self.parking = Parking.objects.create(wing_name='Parking A', is_available=True)
        self.vehicle = VehicleDetail.objects.create(vehicle_number='ABC123', vehicle_type='Sedan', vehicle_brand='Toyota')

        self.parking_detail = ParkingDetail.objects.create(
            parking_wing=self.parking,
            vehicle_arrived_date=timezone.now().date(),
            vehicle_arrived_time=timezone.now().time()
        )
        self.parking_detail.vehicles.add(self.vehicle)

    def create_user(self, email, password, is_staff=True, is_superuser=True, is_employee=True, is_owner=True):
        user = CustomUser.objects.create_user(email=email, password=password)
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.is_employee = is_employee
        user.is_owner = is_owner
        user.save()
        return user

    def get_authentication_header(self, user):
        refresh = RefreshToken.for_user(user)
        return {'HTTP_AUTHORIZATION': f'Bearer {str(refresh.access_token)}'}

    def test_create_parking_detail(self):
        self.client.credentials(**self.get_authentication_header(self.employee_user))
        response = self.client.post(reverse('rest_api:parking_detail_create'), {
            'parking_wing': self.parking.id,
            'vehicle_arrived_date': '2024-01-01',
            'vehicle_arrived_time': '12:00:00'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ParkingDetail.objects.count(), 2)

    def test_list_parking_details(self):
        self.client.credentials(**self.get_authentication_header(self.owner_user))
        response = self.client.get(reverse('rest_api:parking_list'))  # Update route name
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_update_parking_detail(self):
        self.client.credentials(**self.get_authentication_header(self.owner_user))
        response = self.client.patch(
            reverse('rest_api:parking-detail', kwargs={'pk': self.parking_detail.id}),
            {'vehicle_arrived_date': '2024-01-02'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.parking_detail.refresh_from_db()
        self.assertEqual(self.parking_detail.vehicle_arrived_date, datetime.strptime('2024-01-02', '%Y-%m-%d').date())
            
    def test_delete_parking_detail(self):
        self.client.credentials(**self.get_authentication_header(self.owner_user))
        response = self.client.delete(reverse('rest_api:parking-detail', kwargs={'pk': self.parking_detail.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ParkingDetail.objects.count(), 0)
            
# for vehicle details
class VehicleDetailAPITests(APITestCase):

    def setUp(self):
        self.owner_user = self.create_user(email='radar@gmail.com', password='password', is_owner=True)
        
        self.vehicle_owner = VehicleOwner.objects.create(
            user=self.owner_user,
            name='Sure Doe',
            phone_number='1234567890',
            address='123 Street, City'
        )

        self.vehicle1 = VehicleDetail.objects.create(
            vehicle_number='ABC123',
            vehicle_type='Sedan',
            vehicle_brand='Toyota'
        )
        self.vehicle_owner.owned_vehicle = self.vehicle1
        self.vehicle_owner.save()

    def create_user(self, email, password, is_staff=True, is_superuser=True, is_owner=True):
        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_owner=is_owner
        )
        return user

    def get_authentication_header(self, user):
        refresh = RefreshToken.for_user(user)
        return {'HTTP_AUTHORIZATION': f'Bearer {str(refresh.access_token)}'}

    def test_create_vehicle_detail(self):
        self.client.credentials(**self.get_authentication_header(self.owner_user))
        response = self.client.post(
            reverse('rest_api:post-list'),
            {
                'vehicle_number': 'XYZ789',
                'vehicle_type': 'SUV',
                'vehicle_brand': 'Honda',
                'owner': {
                    'name': 'Jane Doe',
                    'phone_number': '0987654321',
                    'address': '456 Another St, City'
                }
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(VehicleDetail.objects.count(), 2)
        
class VehicleDetailAPITests(APITestCase):

    def setUp(self):
        self.owner_user = self.create_user(email='radar@gmail.com', password='password', is_owner=True)
        
        self.vehicle_owner = VehicleOwner.objects.create(
            user=self.owner_user,
            name='Sure Doe',
            phone_number='1234567890',
            address='123 Street, City'
        )

        self.vehicle1 = VehicleDetail.objects.create(
            vehicle_number='ABC123',
            vehicle_type='Sedan',
            vehicle_brand='Toyota'
        )
        self.vehicle_owner.owned_vehicle = self.vehicle1
        self.vehicle_owner.save()

    def create_user(self, email, password, is_staff=True, is_superuser=True, is_owner=True):
        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_owner=is_owner
        )
        return user

    def get_authentication_header(self, user):
        refresh = RefreshToken.for_user(user)
        return {'HTTP_AUTHORIZATION': f'Bearer {str(refresh.access_token)}'}

    def test_create_vehicle_detail(self):
        self.client.credentials(**self.get_authentication_header(self.owner_user))
        response = self.client.post(
            reverse('rest_api:postveh-list'),
            {
                'vehicle_number': 'XYZ789',
                'vehicle_type': 'SUV',
                'vehicle_brand': 'Honda',
                'owner': {
                    'name': 'Jane Doe',
                    'phone_number': '0987654321',
                    'address': '456 Another St, City'
                }
            },
            format='json'  
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(VehicleDetail.objects.count(), 2)
        
    def test_list_vehicle_details(self):
        new_user = self.create_user(email='newuser@gmail.com', password='password', is_owner=True)
        
        new_vehicle = VehicleDetail.objects.create(
            vehicle_number='XYZ789',
            vehicle_type='SUV',
            vehicle_brand='Honda'
        )
        
        VehicleOwner.objects.create(
            user=new_user,
            name='Jane Doe',
            phone_number='0987654321',
            address='456 Another St, City',
            owned_vehicle=new_vehicle
        )

        self.client.credentials(**self.get_authentication_header(self.owner_user))
        response = self.client.get(reverse('rest_api:postveh-list'))


        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


    
# for user auth


class UserCreateAPITests(APITestCase):

    def test_create_user(self):
        response = self.client.post(reverse('rest_api:register'), {'email': 'newuser@example.com', 'password': 'password123'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().email, 'newuser@example.com')

class CustomTokenObtainPairViewTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(email='user@example.com', password='password123')

    def test_obtain_token_pair(self):
        response = self.client.post(reverse('rest_api:token_obtain_pair'), {'email': 'user@example.com', 'password': 'password123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)