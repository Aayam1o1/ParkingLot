from django.urls import path, include
from django.views.generic import ListView

from . import views
from .views import *
from django.conf.urls.i18n import set_language

urlpatterns = [
    path("", views.car_detail_view, name="index"),
    path("parking/", views.parking, name="parking"),
    path("car/", views.car_detail_create, name="car_detail_create"),
    path("edit_cardetail/", views.car_detail_edit, name="car_detail_edit"),
    path("delete_cardetail/", views.car_detail_delete, name="car_detail_delete"),
    path("checkout_cardetail/", views.car_detail_checkout, name="car_detail_checkout"),
    path("parking_edit/", views.parking_edit, name="parking_edit"),
    path("parking_delete/", views.parking_delete, name="parking_delete"),
    # class based urls aba
    path("car_detail/", CarDetailView.as_view(), name="car_detail"),
    path("more_car_detail/", CarDetailMoreView.as_view(), name="more_car_detial"),
    path("owner_profile/", OwnerProfileView.as_view(), name="owner_profile"),
    path('lang',set_language,name='lang'),
    path('set_language/', views.set_language, name='set_language'),
    path('rosetta/', include('rosetta.urls')),


]
