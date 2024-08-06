import logging

from django.contrib.auth import get_user_model
from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_api.filters import ParkingDetailFilter
from rest_api.models import Parking, ParkingDetail, VehicleDetail, VehicleOwner
from rest_api.pagination import *
from rest_api.permissions import IsAdminUser, IsEmployee, IsOwner
from rest_api.serializers import (
    ParkingDetailSerializer,
    ParkingSerializer,
    VehicleDetailSerializer,
)
from rest_api.tasks import send_registration_email
from rest_framework import generics, viewsets
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomTokenObtainPairSerializer, UserSerializer


# Create your views here.
# Generics API
class ParkingCreateAPIView(CreateAPIView):
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class ParkingUpdateAPIView(UpdateAPIView):
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class ParkingListAPIView(ListAPIView, PageNumberPagination):
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsEmployee]
    pagination_class = CustomCursorPagination


class ParkingDestroyAPIView(DestroyAPIView):
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class ParkingRetrieveAPIView(RetrieveAPIView):
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer
    permission_classes = [IsAuthenticated]


# Parking Detail View for Employees
class ParkingDetailCreateAPIView(CreateAPIView):
    queryset = ParkingDetail.objects.all()
    serializer_class = ParkingDetailSerializer
    permission_classes = [IsAuthenticated, IsEmployee, IsAdminUser]
    pagination_class = CustomLimitOffsetPagination


# Viewset
# @method_decorator(csrf_exempt, name='dispatch')


class VehicleDetailViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleDetailSerializer
    # permission_classes = [IsAuthenticated, IsOwner | IsAdminUser]
    pagination_class = CustomLimitOffsetPagination

    def get_queryset(self):
        user = self.request.user
        return VehicleDetail.objects.filter(owner__user=user)


class NoPagination(PageNumberPagination):
    page_size = 1000


class ParkingDetailViewSet(viewsets.ModelViewSet):
    serializer_class = ParkingDetailSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsAdminUser | IsEmployee]
    pagination_class = NoPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ParkingDetailFilter

    def get_queryset(self):
        # Ensure the authenticated user has a VehicleOwner instance associated
        user = self.request.user
        if user.is_superuser:
            return ParkingDetail.objects.all()
        elif hasattr(user, "vehicle_owner"):
            # Filter parking details based on the owner's vehicles
            return ParkingDetail.objects.filter(vehicles__owner=user.vehicle_owner)
        else:
            # Handle case where user does not have a VehicleOwner instance
            return ParkingDetail.objects.none()


User = get_user_model()
logger = logging.getLogger(__name__)


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
