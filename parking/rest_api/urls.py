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
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


app_name = "rest_api"


router = routers.DefaultRouter()
router.register(r"posts", VehicleDetailViewSet, basename="postveh")
router.register(r"parking_spot", ParkingDetailViewSet, basename="parking")
router.register(r'documents', DocumentViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
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
    
