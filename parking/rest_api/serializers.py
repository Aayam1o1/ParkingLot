from rest_framework import serializers
from rest_api.models import Parking, VehicleDetail, ParkingDetail, CustomUser, VehicleOwner
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.models.signals import post_save


class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Parking
        fields = ('id', 'wing_name', 'is_available')
        # fields = '__all__' 
        
        
class VehicleOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleOwner
        fields = ['name', 'phone_number', 'address']

class VehicleDetailSerializer(serializers.ModelSerializer):
    owner = VehicleOwnerSerializer(required=True)

    class Meta:
        model = VehicleDetail
        fields = ['id', 'vehicle_number', 'vehicle_type', 'vehicle_brand', 'owner']

    def create(self, validated_data):
        owner_data = validated_data.pop('owner', None)
        vehicle_detail = VehicleDetail.objects.create(**validated_data)
        
        if owner_data:
            # Assuming 'user_id' is passed in validated_data or obtained from request context
            user_id = self.context['request'].user.id  # Adjust this based on how you handle user authentication
            user = CustomUser.objects.get(id=user_id)
            VehicleOwner.objects.create(user=user, owned_vehicle=vehicle_detail, **owner_data)
            
        return vehicle_detail
        
class ParkingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingDetail
        fields = '__all__'
        
        
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined', 'is_employee', 'is_owner')
    
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