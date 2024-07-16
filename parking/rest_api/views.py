from django.shortcuts import render
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, DestroyAPIView, RetrieveAPIView
from rest_api.models import Parking, VehicleDetail, VehicleOwner, ParkingDetail
from rest_api.serializers import ParkingSerializer, VehicleDetailSerializer, ParkingDetailSerializer
from rest_framework import viewsets
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from rest_framework.permissions import BasePermission
from rest_api.permissions import IsAdminUser, IsEmployee, IsOwner
from rest_framework.permissions import IsAuthenticated


# Create your views here.
# Generics API
class ParkingCreateAPIView(CreateAPIView):
    queryset=Parking.objects.all()
    serializer_class=ParkingSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class ParkingUpdateAPIView(UpdateAPIView):
    queryset=Parking.objects.all()
    serializer_class=ParkingSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class ParkingListAPIView(ListAPIView):
    queryset=Parking.objects.all()
    serializer_class=ParkingSerializer
    permission_classes = [IsAuthenticated, IsAdminUser, IsEmployee]



class ParkingDestroyAPIView(DestroyAPIView):
    queryset = Parking.objects.all()
    serializer_class=ParkingSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class ParkingRetrieveAPIView(RetrieveAPIView):
    queryset = Parking.objects.all()
    serializer_class=ParkingSerializer
    permission_classes = [IsAuthenticated]


# Parking Detail View for Employees
class ParkingDetailCreateAPIView(CreateAPIView):
    queryset = ParkingDetail.objects.all()
    serializer_class = ParkingDetailSerializer
    permission_classes = [IsAuthenticated, IsEmployee, IsAdminUser]
  
    
# Viewset
# @method_decorator(csrf_exempt, name='dispatch')

class VehicleDetailViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleDetailSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return VehicleDetail.objects.filter(owner=self.request.user)
    
       
class ParkingDetailViewSet(viewsets.ModelViewSet):
    serializer_class = ParkingDetailSerializer
    permission_classes = [IsAuthenticated, IsOwner]  

    def get_queryset(self):
        # Ensure the authenticated user has a VehicleOwner instance associated
        user = self.request.user
        if hasattr(user, 'vehicle_owner'):
            # Filter parking details based on the owner's vehicles
            return ParkingDetail.objects.filter(vehicles__owner=user.vehicle_owner)
        else:
            # Handle case where user does not have a VehicleOwner instance
            return ParkingDetail.objects.none()
    

User = get_user_model()

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
