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


class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = ("id", "wing_name", "is_available")
        # fields = '__all__'


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
