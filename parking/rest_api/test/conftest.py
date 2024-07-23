import pytest
from rest_framework.test import APIClient
from rest_api.factories import CustomUserFactory, ParkingFactory, VehicleDetailFactory, ParkingDetailFactory

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user():
    return CustomUserFactory(is_staff=True, is_superuser=True)

@pytest.fixture
def employee_user():
    return CustomUserFactory(is_staff=True)

@pytest.fixture
def client_user():
    return CustomUserFactory()

@pytest.fixture
def parking():
    return ParkingFactory()


@pytest.fixture
def vehicle_detail():
    return VehicleDetailFactory()

@pytest.fixture
def parking_detail(parking, vehicle_detail):
    parking_detail = ParkingDetailFactory(parking_wing=parking)
    parking_detail.vehicles.set([vehicle_detail])
    parking_detail.save()
    return parking_detail