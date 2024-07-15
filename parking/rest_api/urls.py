from django.urls import path
from rest_api.views import ParkingCreateAPIView, ParkingUpdateAPIView, ParkingListAPIView, ParkingDestroyAPIView, ParkingRetrieveAPIView

urlpatterns = [
    path('parking/create/', ParkingCreateAPIView.as_view(), name='parking_create'),
    path('parking/update/<pk>/',ParkingUpdateAPIView.as_view(), name='parking_update'),
    path('parking_list/',ParkingListAPIView.as_view(), name='parking_list'),
    path('parking_delete/<pk>/', ParkingDestroyAPIView.as_view(), name='parking_delete'),
    path('parking/retrieve/<pk>/', ParkingRetrieveAPIView.as_view(), name='parking_retrive'),
]