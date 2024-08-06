import pytest
from rest_framework import status
from django.urls import reverse
from rest_api.models import Parking, VehicleOwner, VehicleDetail, ParkingDetail
from rest_api.factories import CustomUserFactory, VehicleDetailFactory, VehicleOwnerFactory

@pytest.mark.django_db
class TestParkingAPI:
    def test_create_parking(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        response = api_client.post(reverse('rest_api:parking_create'), {'wing_name': 'B', 'is_available': False})
        assert response.status_code == status.HTTP_201_CREATED
        assert Parking.objects.count() == 1

    def test_update_parking(self, api_client, admin_user, parking):
        api_client.force_authenticate(user=admin_user)
        response = api_client.patch(reverse('rest_api:parking_update', kwargs={'pk': parking.id}), {'wing_name': 'C'})
        assert response.status_code == status.HTTP_200_OK
        parking.refresh_from_db()
        assert parking.wing_name == 'C'

    def test_list_parking(self, api_client, employee_user, parking):
        api_client.force_authenticate(user=employee_user)
        response = api_client.get(reverse('rest_api:parking_list'))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

    def test_retrieve_parking(self, api_client, employee_user, parking):
        api_client.force_authenticate(user=employee_user)
        response = api_client.get(reverse('rest_api:parking_retrive', kwargs={'pk': parking.id}))
        assert response.status_code == status.HTTP_200_OK
        assert response.data['wing_name'] == parking.wing_name

    def test_delete_parking(self, api_client, admin_user, parking):
        api_client.force_authenticate(user=admin_user)
        response = api_client.delete(reverse('rest_api:parking_delete', kwargs={'pk': parking.id}))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Parking.objects.count() == 0

    def test_vehicle_list(self, api_client, client_user):
        api_client.force_authenticate(user=client_user)
        response = api_client.get(reverse('rest_api:postveh-list'))
        assert response.status_code == status.HTTP_200_OK

    def test_user_registration(self, api_client):
        response = api_client.post(reverse('rest_api:register'), {'email': 'newuser@example.com', 'password': 'password'})
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestTokenAPI:
    def test_token_obtain_pair(self, api_client):
        user = CustomUserFactory(email='newuser@example.com', password='password')
        user.set_password('password')  
        user.save()

        response = api_client.post(reverse('rest_api:token_obtain_pair'), {'email': 'newuser@example.com', 'password': 'password'})
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_token_refresh(self, api_client):
        user = CustomUserFactory(email='newuser@example.com', password='password')
        user.set_password('password')
        user.save()

        token_response = api_client.post(reverse('rest_api:token_obtain_pair'), {'email': 'newuser@example.com', 'password': 'password'})
        refresh_token = token_response.data.get('refresh')
        if refresh_token:
            response = api_client.post(reverse('rest_api:token_refresh'), {'refresh': refresh_token})
            assert response.status_code == status.HTTP_200_OK
            assert 'access' in response.data
        else:
            pytest.fail('No refresh token returned')

    def test_token_verify(self, api_client):
        # Create and authenticate user
        user = CustomUserFactory(email='newuser@example.com', password='password')
        user.set_password('password')
        user.save()
        token_response = api_client.post(reverse('rest_api:token_obtain_pair'), {'email': 'newuser@example.com', 'password': 'password'})
        access_token = token_response.data.get('access')
        if access_token:
            response = api_client.post(reverse('rest_api:token_verify'), {'token': access_token})
            assert response.status_code == status.HTTP_200_OK
        else:
            pytest.fail('No access token returned')


@pytest.mark.django_db
class TestVehicleDetailAPI:

    def test_create_vehicle_detail(self, api_client, client_user):
        owner, created = VehicleOwner.objects.get_or_create(
            user=client_user,
            defaults={
                'name': 'Aayam',
                'phone_number': '984000',
                'address': 'dallu'
            }
        )

        vehicle_detail, created = VehicleDetail.objects.get_or_create(
            vehicle_number='Ba-ga-1000',
            vehicle_type='bike',
            vehicle_brand='MT'
        )

        owner.owned_vehicle = vehicle_detail
        owner.save()

        # Serialize the vehicle_detail object to get a dictionary of its data
        vehicle_data = {
            'vehicle_number': vehicle_detail.vehicle_number,
            'vehicle_type': vehicle_detail.vehicle_type,
            'vehicle_brand': vehicle_detail.vehicle_brand,
            'owner': {
                'name': owner.name,
                'phone_number': owner.phone_number,
                'address': owner.address,
            }
        }

        api_client.force_authenticate(user=client_user)  
        response = api_client.post(reverse('rest_api:postveh-list'), vehicle_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert VehicleDetail.objects.count() == 2  

    def test_list_vehicle_details(self, api_client, client_user):
        # Create a VehicleDetail instance and associate it with client_user
        owner = VehicleOwnerFactory(user=client_user)
        vehicle_detail = owner.owned_vehicle

        api_client.force_authenticate(user=client_user)
        response = api_client.get(reverse('rest_api:postveh-list'))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) > 0
        
        
        
@pytest.mark.django_db
class TestParkingDetailAPI:

    def test_create_parking_detail(self, api_client, client_user, parking, vehicle_detail):
        api_client.force_authenticate(user=client_user)
        parking_detail_data = {
            'parking_wing': parking.id,
            'vehicle_arrived_date': '2023-01-01',
            'vehicle_arrived_time': '12:00:00',
            'vehicles': [vehicle_detail.id],
        }
        response = api_client.post(reverse('rest_api:parking-list'), parking_detail_data, format='json')
        print("respomse", response.data)
        assert response.status_code == status.HTTP_201_CREATED
        assert ParkingDetail.objects.count() == 1

    def test_list_parking_details(self, api_client, client_user, parking, vehicle_detail):
        # Create a ParkingDetail instance to list
        api_client.force_authenticate(user=client_user)
        parking_detail_data = {
            'parking_wing': parking.id,
            'vehicle_arrived_date': '2023-01-01',
            'vehicle_arrived_time': '12:00:00',
            'vehicles': [vehicle_detail.id],
        }
        api_client.post(reverse('rest_api:parking-list'), parking_detail_data, format='json')

        # List ParkingDetail instances
        response = api_client.get(reverse('rest_api:parking-list'))
        print("Response Status Code:", response.status_code)
        print("Response Data 2nd:", response.data)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0

    def test_retrieve_parking_detail(self, api_client, client_user, admin_user, parking_detail):
        api_client.force_authenticate(user=admin_user)

        retrieve_url = reverse('rest_api:parking-detail', kwargs={'pk': parking_detail.id})
        response = api_client.get(retrieve_url)
        print("Retrieve Response Status Code:", response.status_code)
        print("Retrieve Response Data:", response.data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == parking_detail.id

    def test_update_parking_detail(self, api_client, admin_user, parking_detail):
        api_client.force_authenticate(user=admin_user)
        response = api_client.patch(reverse('rest_api:parking-detail', kwargs={'pk': parking_detail.id}), {'vehicle_has_left': True}, format='json')
        assert response.status_code == status.HTTP_200_OK
        parking_detail.refresh_from_db()
        assert parking_detail.vehicle_has_left is True

    def test_delete_parking_detail(self, api_client, admin_user, parking_detail):
        api_client.force_authenticate(user=admin_user)
        response = api_client.delete(reverse('rest_api:parking-detail', kwargs={'pk': parking_detail.id}))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert ParkingDetail.objects.count() == 0