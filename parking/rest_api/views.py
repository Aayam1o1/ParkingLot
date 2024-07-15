from django.shortcuts import render
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, DestroyAPIView, RetrieveAPIView
from rest_api.models import Parking, VehicleDetail, VehicleOwner, ParkingDetail
from rest_api.serializers import ParkingSerializer, VehicleDetailSerializer, ParkingDetailSerializer
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.
# Generics API
class ParkingCreateAPIView(CreateAPIView):
    queryset=Parking.objects.all()
    serializer_class=ParkingSerializer


class ParkingUpdateAPIView(UpdateAPIView):
    queryset=Parking.objects.all()
    serializer_class=ParkingSerializer

class ParkingListAPIView(ListAPIView):
    queryset=Parking.objects.all()
    serializer_class=ParkingSerializer


class ParkingDestroyAPIView(DestroyAPIView):
    queryset = Parking.objects.all()
    serializer_class=ParkingSerializer

class ParkingRetrieveAPIView(RetrieveAPIView):
    queryset = Parking.objects.all()
    serializer_class=ParkingSerializer
    
    
    
# Viewset
# @method_decorator(csrf_exempt, name='dispatch')

class VehicleDetailViewSet(viewsets.ModelViewSet):
    queryset = VehicleDetail.objects.all()
    serializer_class  = VehicleDetailSerializer
    
    
class ParkingDetailViewSet(viewsets.ModelViewSet):
    queryset = ParkingDetail.objects.all()
    serializer_class = ParkingDetailSerializer 