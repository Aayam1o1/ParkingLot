import logging

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from rest_api.models import (
    CustomUser,
    Parking,
    ParkingDetail,
    VehicleDetail,
    VehicleOwner,
    
)
from rest_api.tasks import send_registration_email
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_api.models import Document, Comment


class ParkingSerializer(serializers.ModelSerializer):
    wing_name_en = serializers.CharField(required=True, allow_null=False)
    wing_name_ne = serializers.CharField(required=True, allow_null=False)

    class Meta:
        model = Parking
        fields = ("id", "wing_name_en", "wing_name_ne", "is_available")

    def create(self, validated_data):
        wing_name_en = validated_data.pop('wing_name_en', None)

        # Set wing_name to wing_name_en if provided
        if wing_name_en is not None:
            validated_data['wing_name'] = wing_name_en

        # Create the Parking instance
        instance = super().create(validated_data)
        return instance

    def update(self, instance, validated_data):
        wing_name_en = validated_data.pop('wing_name_en', None)

        # Update wing_name if wing_name_en is provided
        if wing_name_en is not None:
            instance.wing_name = wing_name_en

        # Update other fields
        instance.is_available = validated_data.get('is_available', instance.is_available)

        instance.save()
        return instance
    
    def to_representation(self, instance):
        # Call the parent method to get the initial representation
        representation = super().to_representation(instance)

        # Check if the request path contains 'ne'
        request = self.context.get('request')
        if request and 'ne' in request.path:
            return {
                'id': representation['id'],
                'wing_name_ne': representation['wing_name_ne'],
                'is_available': representation['is_available']
            }
        else:
            return {
                'id': representation['id'],
                'wing_name_en': representation['wing_name_en'],
                'is_available': representation['is_available']
            }
class VehicleOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleOwner
        fields = ["name", "phone_number", "address"]


# class VehicleDetailSerializer(serializers.ModelSerializer):
#     owner = VehicleOwnerSerializer(required=True)

#     class Meta:
#         model = VehicleDetail
#         fields = ["id", "vehicle_number", "vehicle_type", "vehicle_brand", "owner"]

#     def create(self, validated_data):
#         owner_data = validated_data.pop("owner", None)
#         vehicle_detail = VehicleDetail.objects.create(**validated_data)

#         if owner_data:
#             user_id = self.context["request"].user.id
#             user = CustomUser.objects.get(id=user_id)

#             # Check if VehicleOwner instance already exists for this user
#             vehicle_owner, created = VehicleOwner.objects.get_or_create(
#                 user=user,
#                 defaults=owner_data
#             )
#             if not created:
#                 # Update the existing VehicleOwner instance if needed
#                 for attr, value in owner_data.items():
#                     setattr(vehicle_owner, attr, value)
#                 vehicle_owner.save()

#             vehicle_detail.owner = vehicle_owner
#             vehicle_detail.save()

#         return vehicle_detail


class VehicleDetailSerializer(serializers.ModelSerializer):
    owner = VehicleOwnerSerializer(required=True)

    class Meta:
        model = VehicleDetail
        fields = ["id", "vehicle_number", "vehicle_type", "vehicle_brand", "owner"]

    def create(self, validated_data):
        owner_data = validated_data.pop("owner", None)
        vehicle_detail = VehicleDetail.objects.create(**validated_data)

        if owner_data:
            user_id = self.context["request"].user.id
            user = CustomUser.objects.get(id=user_id)

            vehicle_owner, created = VehicleOwner.objects.get_or_create(
                user=user, defaults=owner_data
            )
            if not created:
                for attr, value in owner_data.items():
                    setattr(vehicle_owner, attr, value)
                vehicle_owner.save()

            vehicle_owner.owned_vehicle = vehicle_detail
            vehicle_owner.save()

        return vehicle_detail


class ParkingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingDetail
        fields = "__all__"


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "date_joined",
            "is_employee",
            "is_owner",
        )

    def create(self, validated_data):
        # user = CustomUser.objects.create_user(**validated_data)
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            is_employee=validated_data.get("is_employee", False),
            is_owner=validated_data.get("is_owner", False),
        )

        send_registration_email.delay(validated_data["email"])

        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token["email"] = user.email
        return token


class ParkingReportSerializer(serializers.Serializer):
    file = serializers.FileField()
    

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'file']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'page', 'x1', 'y1', 'x2', 'y2', 'whole_page', 'document']