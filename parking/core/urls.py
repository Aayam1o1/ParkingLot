from django.urls import path
from . import views
from django.views.generic import ListView
from .views import *



urlpatterns = [
    path("", views.car_detail_view, name="index"),
    path("parking", views.parking, name="parking"),
    path("car", views.car_detail_create, name="car_detail_create"),
    path('edit_cardetail/', views.car_detail_edit, name='car_detail_edit'),
    path('delete_cardetail/', views.car_detail_delete, name='car_detail_delete'),
    path('checkout_cardetail/', views.car_detail_checkout, name='car_detail_checkout'),
    path('parking_edit/', views.parking_edit, name='parking_edit'),
    path('parking_delete/', views.parking_delete, name='parking_delete'),


    # class based urls aba
    path("index2", car_detail_view.as_view(), name='index2'),
    path("more_car_detail", car_detail_more_view.as_view(), name='more_car_detial')

    

]
    