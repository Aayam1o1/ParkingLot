from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_api.models import CustomUser, Parking, VehicleDetail, ParkingDetail
from django.utils import timezone
from datetime import datetime


class ParkingAPITests(APITestCase):
    def setUp(self):
        self.admin_user = self.create_user(email='admin@example.com', password='password', is_staff=True, is_superuser=True)
        self.employee_user = self.create_user(email='employee@example.com', password='password', is_staff=True)
        self.parking = Parking.objects.create(wing_name='A', is_available=True)
        self.client_user = self.create_user(email='client@example.com', password='password')
        self.vehicle_detail = VehicleDetail.objects.create(
            vehicle_number='ABC123',
            vehicle_type='Sedan',
            vehicle_brand='Toyota'
        )
        self.parking_detail = ParkingDetail.objects.create(
            parking_wing=self.parking,
            vehicle_arrived_date=timezone.now().date(),
            vehicle_arrived_time=timezone.now().time()
        )
        self.parking_detail.vehicles.add(self.vehicle_detail)
       
        
    def create_user(self, email, password, is_staff=False, is_superuser=False):
        user = CustomUser.objects.create_user(email=email, password=password)
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()
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
        self.client.force_authenticate(user=self.employee_user)
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

    def test_vehicle_list(self):
        self.client.force_authenticate(user=self.client_user)
        response = self.client.get(reverse('rest_api:postveh-list')) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_parking_detail_list(self):
        self.client.force_authenticate(user=self.client_user)
        response = self.client.get(reverse('rest_api:parking-list'))  
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_registration(self):
        response = self.client.post(reverse('rest_api:register'), {'email': 'newuser@example.com', 'password': 'password'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_token_obtain_pair(self):
        response = self.client.post(reverse('rest_api:token_obtain_pair'), {'email': 'admin@example.com', 'password': 'password'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)


    def test_token_refresh(self):
        token_response = self.client.post(reverse('rest_api:token_obtain_pair'), {'email': 'admin@example.com', 'password': 'password'})
        refresh_token = token_response.data.get('refresh')
        if refresh_token:  # Make sure refresh token is obtained
            response = self.client.post(reverse('rest_api:token_refresh'), {'refresh': refresh_token})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn('access', response.data)
        else:
            self.fail('No refresh token returned')

    def test_token_verify(self):
        token_response = self.client.post(reverse('rest_api:token_obtain_pair'), {'email': 'admin@example.com', 'password': 'password'})
        access_token = token_response.data.get('access')
        if access_token:  # Make sure access token is obtained
            response = self.client.post(reverse('rest_api:token_verify'), {'token': access_token})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        else:
            self.fail('No access token returned')
