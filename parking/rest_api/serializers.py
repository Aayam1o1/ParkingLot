from rest_framework import serializers
from rest_api.models import Parking, VehicleDetail, ParkingDetail

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