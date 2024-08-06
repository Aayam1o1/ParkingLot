from django.urls import include, path
from rest_api.views import (
    CustomTokenObtainPairView,
    ParkingCreateAPIView,
    ParkingDestroyAPIView,
    ParkingDetailCreateAPIView,
    ParkingDetailViewSet,
    ParkingListAPIView,
    ParkingRetrieveAPIView,
    ParkingUpdateAPIView,
    UserCreateView,
    VehicleDetailViewSet,
    ExportParkingReport,
    ImportParkingReport,
    DocumentViewSet,
    CommentViewSet,
    
)
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

app_name = "rest_api"


router = routers.DefaultRouter()
router.register(r"posts", VehicleDetailViewSet, basename="postveh")
router.register(r"parking_spot", ParkingDetailViewSet, basename="parking")
router.register(r'documents', DocumentViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path("parking/create/", ParkingCreateAPIView.as_view(), name="parking_create"),
    path("parking/update/<pk>/", ParkingUpdateAPIView.as_view(), name="parking_update"),
    path("parking_list/", ParkingListAPIView.as_view(), name="parking_list"),
    path("parking_list/ne/", ParkingListAPIView.as_view(), name="parking_list_ne"),

    path(
        "parking_delete/<pk>/", ParkingDestroyAPIView.as_view(), name="parking_delete"
    ),
    path(
        "parking/retrieve/<pk>/",
        ParkingRetrieveAPIView.as_view(),
        name="parking_retrive",
    ),
    path(
        "parking/detail/create/",
        ParkingDetailCreateAPIView.as_view(),
        name="parking_detail_create",
    ),
    # for viewset
    path("", include(router.urls)),
    # for JWT
    path("api/register/", UserCreateView.as_view(), name="register"),
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    
    # for import export
    path('export/parking_reports/', ExportParkingReport, name='export_parking_reports'),
    path('import/parking_reports/', ImportParkingReport.as_view(), name='import_parking_reports'),
]
    
