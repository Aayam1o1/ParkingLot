from rest_framework import serializers
from rest_api.models import Parking, VehicleDetail, ParkingDetail, CustomUser
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Parking
        fields = ['id', 'wing_name', 'is_available']
        # fields = '__all__' 
        
        
        
class VehicleDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = VehicleDetail
        fields = ['id', 'vehicle_number', 'vehicle_type', 'vehicle_brand']
        
        
class ParkingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingDetail
        fields = '__all__'
        
        
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined')
    
    def create(self,  validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        print("🐍 File: rest_api/serializers.py | Line: 37 | create ~ validated_data",validated_data)
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        return token