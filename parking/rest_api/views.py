from django.shortcuts import render
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, DestroyAPIView, RetrieveAPIView
from rest_api.models import Parking
from rest_api.serializers import ParkingSerializer

# Create your views here.

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
