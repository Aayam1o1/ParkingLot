from django.urls import path
from . import views



urlpatterns = [
    path("", views.index, name="index"),
    path("parking", views.parking, name="parking"),
    path("car", views.car, name="car"),
    path('edit_cardetail/', views.edit_car, name='edit_car'),  # No car_id in URL pattern
    path('delete_cardetail/', views.delete_car, name='delete_car')
]
    