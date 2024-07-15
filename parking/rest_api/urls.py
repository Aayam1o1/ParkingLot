from django.urls import path, include
from rest_framework import routers
from rest_api.views import ParkingCreateAPIView, ParkingUpdateAPIView, ParkingListAPIView, ParkingDestroyAPIView, ParkingRetrieveAPIView, VehicleDetailViewSet, ParkingDetailViewSet, UserCreateView, CustomTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenVerifyView

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
    
    
    # for JWT
    path('api/register/', UserCreateView.as_view(), name='register'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]