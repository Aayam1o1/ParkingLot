from django_filters import rest_framework as filters

from .models import ParkingDetail


class ParkingDetailFilter(filters.FilterSet):
    parking_wing_id = filters.NumberFilter(
        field_name="parking_wing__id", lookup_expr="exact"
    )
    parking_wing_name = filters.CharFilter(
        field_name="parking_wing__wing_name", lookup_expr="exact"
    )

    class Meta:
        model = ParkingDetail
        fields = ["parking_wing_id", "parking_wing_name"]


class ParkingDetailFilter(filters.FilterSet):
    parking_wing = filters.CharFilter(method="filter_parking_wing")

    def filter_parking_wing(self, queryset, name, value):
        if value.startswith("'") and value.endswith("'"):
            value = value[1:-1]

        try:
            return queryset.filter(parking_wing__id=int(value))
        except ValueError:
            return queryset.filter(parking_wing__wing_name=value)

    class Meta:
        model = ParkingDetail
        fields = ["parking_wing"]
