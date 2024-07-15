from rest_framework import serializers
from rest_api.models import Parking

class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Parking
        fields = ['id', 'wing_name', 'is_available']
        # fields = '__all__' 