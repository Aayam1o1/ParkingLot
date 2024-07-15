from django.urls import path, include
from rest_framework import routers
from rest_api.views import ParkingCreateAPIView, ParkingUpdateAPIView, ParkingListAPIView, ParkingDestroyAPIView, ParkingRetrieveAPIView, VehicleDetailViewSet, ParkingDetailViewSet


router = routers.DefaultRouter()
router.register(r'posts', VehicleDetailViewSet, basename="post")
router.register(r'parking_spot', ParkingDetailViewSet, basename="parking")

urlpatterns = [
    path('parking/create/', ParkingCreateAPIView.as_view(), name='parking_create'),
    path('parking/update/<pk>/',ParkingUpdateAPIView.as_view(), name='parking_update'),
    path('parking_list/',ParkingListAPIView.as_view(), name='parking_list'),
    path('parking_delete/<pk>/', ParkingDestroyAPIView.as_view(), name='parking_delete'),
    path('parking/retrieve/<pk>/', ParkingRetrieveAPIView.as_view(), name='parking_retrive'),
    
    
    # for viewset
    path('', include(router.urls)),
    
    
    

]