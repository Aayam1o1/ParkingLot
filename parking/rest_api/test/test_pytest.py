import pytest
from rest_framework.test import APIClient
from rest_framework import status
from rest_api.models import CustomUser, Parking, VehicleDetail, ParkingDetail, VehicleOwner
from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

@pytest.fixture
def setup_data():
    # Setup your data here
    admin_user = CustomUser.objects.create_user(email='aayam@gmail.com', password='aayam', is_staff=True, is_superuser=True, is_employee=True, is_owner=True, is_active=True)
    employee_user = CustomUser.objects.create_user(email='employee@example.com', password='password', is_staff=True)
    client_user = CustomUser.objects.create_user(email='client@example.com', password='password')
    print("Admin User:", admin_user)  # Debugging line

    parking = Parking.objects.create(wing_name='A', is_available=True)
    vehicle_detail = VehicleDetail.objects.create(
        vehicle_number='Ba-ga-1000',
        vehicle_type='bike',
        vehicle_brand='MT'
    )
    parking_detail = ParkingDetail.objects.create(
        parking_wing=parking,
        vehicle_arrived_date=timezone.now().date(),
        vehicle_arrived_time=timezone.now().time()
    )
    parking_detail.vehicles.add(vehicle_detail)
    
    return {
        'admin_user': admin_user,
        'employee_user': employee_user,
        'client_user': client_user,
        'parking': parking,
        'vehicle_detail': vehicle_detail,
        'parking_detail': parking_detail
    }
    
    
# @pytest.fixture(autouse=True)
# def create_user():
#     # Setup your data here
#     admin_user = CustomUser.objects.get_or_create(email='aayam@gmail.com', password='aayam', is_staff=True, is_superuser=True, is_employee=True, is_owner=True, is_active=True)
   
    
  
#     return admin_user

# @pytest.fixture()
# def create_vehicle():
#     # Setup your data here
   
#     vehicle_detail = VehicleDetail.objects.create(
#         vehicle_number='Ba-ga-1000',
#         vehicle_type='bike',
#         vehicle_brand='MT'
#     )
  
#     return vehicle_detail
    
User = get_user_model()

@pytest.mark.django_db
def test_partial_update_vehicle_detail():
    client = APIClient()
    admin_user = User.objects.create_user(email='aayam@gmail.com', password='aayam', is_staff=True, is_superuser=True, is_employee=True, is_owner=True, is_active=True)
    client.force_authenticate(user=admin_user)

    owner, created = VehicleOwner.objects.get_or_create(
        user=admin_user,
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

    print("owner", owner)
    print("vehicle_detail", vehicle_detail)
    vehicle_id = vehicle_detail.id
    url = f"/posts/{vehicle_id}/"  # Adjust the URL to match your routing
    response = client.patch(url, {'vehicle_type': 'sure'}, format="json")

    print("🐍 File: test/test_pytest.py | Line: 82 | test_partial_update_vehicle_detail ~ response", response.data)
    assert response.status_code == status.HTTP_200_OK

    
    
# @pytest.mark.django_db

# def test_partial_update_parking_detail():
#     client = APIClient()
#     admin_user = CustomUser.objects.create_user(email='aayam@gmail.com', password='aayam', is_staff=True, is_superuser=True, is_employee=True, is_owner=True, is_active=True)
#     client.force_authenticate(user=admin_user)
   
#     parking_wing = Parking.objects.create(
#         wing_name = 'A1',
#         is_available = True
#     )
    
#     print(Parking.objects.filter(pk=1),'askldf')
#     parking_id = ParkingDetail.id
#     print("parking_id", parking_id)
#     url = reverse("rest_api:parking_update",kwargs={"pk": 1})
#     print(f"Updating vehicle at URL: {url}") 
#     response = client.patch(url, {'wing_name': 'sure'}, format = "json")
#     print(f"Response status code: {response.status_code}")  # Debugging line
#     print(f"Response data: {response.data}") 
#     print(response.data)
#     assert response.status_code == status.HTTP_200_OK


    
@pytest.mark.django_db
def test_create_parking(setup_data):
    client = APIClient()
    client.force_authenticate(user=setup_data['admin_user'])
    response = client.post('/parking/create/', {'wing_name': 'B', 'is_available': False})
    assert response.status_code == status.HTTP_201_CREATED
    assert Parking.objects.count() == 2

@pytest.mark.django_db
def test_update_parking(setup_data):
    client = APIClient()
    client.force_authenticate(user=setup_data['admin_user'])
    response = client.patch(f'/parking/update/{setup_data["parking"].id}/', {'wing_name': 'C'})
    assert response.status_code == status.HTTP_200_OK
    setup_data['parking'].refresh_from_db()
    assert setup_data['parking'].wing_name == 'C'






@pytest.mark.django_db
def test_list_parking(setup_data):
    client = APIClient()
    client.force_authenticate(user=setup_data['employee_user'])
    response = client.get('/parking_list/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 1

@pytest.mark.django_db
def test_retrieve_parking(setup_data):
    client = APIClient()
    client.force_authenticate(user=setup_data['employee_user'])
    response = client.get(f'/parking/retrieve/{setup_data["parking"].id}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['wing_name'] == 'A'

@pytest.mark.django_db
def test_delete_parking(setup_data):
    client = APIClient()
    client.force_authenticate(user=setup_data['admin_user'])
    response = client.delete(f'/parking_delete/{setup_data["parking"].id}/')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Parking.objects.count() == 0

@pytest.mark.django_db
def test_vehicle_list(setup_data):
    client = APIClient()
    client.force_authenticate(user=setup_data['client_user'])
    response = client.get('/posts/')
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_parking_detail_list(setup_data):
    client = APIClient()
    client.force_authenticate(user=setup_data['client_user'])
    response = client.get('/parking/')
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_user_registration():
    client = APIClient()
    response = client.post('/api/register/', {'email': 'aayam@gmail.com', 'password': 'aayam'})
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_token_obtain_pair(setup_data):
    client = APIClient()
    response = client.post('/api/token/', {'email': 'aayam@gmail.com', 'password': 'aayam'})
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data

@pytest.mark.django_db
def test_token_refresh(setup_data):
    client = APIClient()
    token_response = client.post('/api/token/', {'email': 'aayam@gmail.com', 'password': 'aayam'})
    refresh_token = token_response.data.get('refresh')
    assert refresh_token is not None
    response = client.post('/api/token/refresh/', {'refresh': refresh_token})
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data

@pytest.mark.django_db
def test_token_verify(setup_data):
    client = APIClient()
    token_response = client.post('/api/token/', {'email': 'aayam@gmail.com', 'password': 'aayam'})
    access_token = token_response.data.get('access')
    assert access_token is not None
    response = client.post('/api/token/verify/', {'token': access_token})
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_create_parking_invalid_data(setup_data):
    client = APIClient()
    client.force_authenticate(user=setup_data['admin_user'])
    response = client.post('/parking/create/', {'wing_name': ''})  
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    

