from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from .forms import addVehicleForm, parkingWingForm, editVehicleForm
from .models import *
from django.views.generic import ListView, DetailView
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.signals import request_finished
import sweetify



def car_detail_view(request):
    """
    This function is used to view the car, parking details in the index or 
    home page.
    
    parameter: request
    
    return: webpage index to render car and wing details
    """
    
    cars = CarDetail.objects.all()
    wings = Parking.objects.filter(is_available=True)
    parking = ParkingDetail.objects.all()
    context = {
        'cars': cars,
        'wings': wings,
        'parking':parking,
    }
    return render(request, 'index.html', context)


def parking(request):
    """
    This function is used to get the details of parking wing and create new parking spots
    and display the wings in template.
    
    parameter: request
    
    return: webpage parking to render car and wing details

    """
    
    wings = Parking.objects.all()

    parking_details = ParkingDetail.objects.all()

    if request.method == "POST":
        form = parkingWingForm(request.POST)
        
        if form.is_valid():
            
            form.save()
            return redirect('/')

    else:
        form = parkingWingForm()
    
    context = {
        'form': form,
        'wings': wings,
        'parking_details': parking_details,
    }

    return render(request, 'parking.html', context)


def car_detail_create(request):
    """
    This function is used insert new car into the parking sytem
    This function uses form addVehicleForm consisting of data like owner name, phone number,
    vehicle number, vehicle type and parking wing.
    
    parameter: request
    
    return: webpage car to render vehicle form.
    """
    if request.method == "POST":
        form = addVehicleForm(request.POST)
        
        if form.is_valid():
            parking_wing=form.cleaned_data['parking_wing']
            
            if ParkingDetail.objects.filter(parking_wing=parking_wing, vehicle_left_date__isnull=True).exists():
                sweetify.error(request, 'The space is occupied already please choose another parking wing')
                return redirect('car_detail_create')
            
            car_detail = form.save() 
            parking_detail = ParkingDetail.objects.create(
                vehicle_number=car_detail,
                parking_wing=parking_wing,
                vehicle_arrived_date=timezone.now()  
            
            )
            
            
            return redirect('/')
    else:
        form = addVehicleForm()

    return render(request, 'car.html', {'form': form})


def car_detail_edit(request):
    """
    This function is used edit car details
    This function uses form editVehicleForm consisting of data like owner name, phone number,
    vehicle number, vehicle type and parking wing.
    
    parameter: request
    
    return redirect "/"    
    
    """
    if request.method == "POST":
        car_id = request.POST.get('car_id')
        car = get_object_or_404(CarDetail, id=car_id)
        form = editVehicleForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            return redirect('/')  
        else:
            wings = Parking.objects.filter(is_available=True)
            cars = CarDetail.objects.all()
            context = {
                'cars': cars,
                'wings': wings,
                'form': form,
                'car': car,
            }
            return render(request, 'index.html', context)
    return redirect('/')

def car_detail_checkout(request):
    """
    This function is used to check out the car from the parking lot.
    Helps in setting the car left date and time.
    
    parmeter: request
    
    return redirect('/')
    
    """
    if request.method == "POST":
        car_id = request.POST.get('car_id')
        vehicle = get_object_or_404(CarDetail, id=car_id)
        
        parking_detail = get_object_or_404(ParkingDetail, vehicle_number=vehicle)
        
        
        if not parking_detail.vehicle_has_left:

            parking_detail.vehicle_has_left = True
            parking_detail.vehicle_left_date = timezone.now()
            parking_detail.vehicle_left_time = timezone.now()
            parking_detail.save()
    
    return redirect('/')


def car_detail_delete(request):
    """
    This function is used to delete the car from the system
    
    parameters: request
    
    return redirect('/')
    """
    
    if request.method == "POST":
        car_id = request.POST.get('car_id')
        car = get_object_or_404(CarDetail, id=car_id)
        
        car.delete()
    
    return redirect('/')


def parking_edit(request):
    """
    This function is used edit parking details
    This function uses form parkingWingForm consisting of data wing_name
    
    parameter: request
    
    return redirect "/"    
    
    """
    if request.method == "POST":
        wing_id = request.POST.get('wing_id')
        wing = get_object_or_404(Parking, id=wing_id)
        form = parkingWingForm(request.POST, instance=wing)
        
        
        if form.is_valid():
            form.save()
            return redirect('parking')  
        else:
            wings = Parking.objects.filter(is_available=True)
            context = {
                'wings': wings,
                'form': form,
                'wing': wing,
            }
            return render(request, 'parking.html', context)
    return redirect('/')

def parking_delete(request):
    """
    This function is used to delete the parking wing name from the system
    
    parameters: request
    
    return redirect('/')
    """
    if request.method == "POST":
        wing_id = request.POST.get('wing_id')
        wing = get_object_or_404(Parking, id=wing_id)
        
        wing.delete()
    
    return redirect('/')




# From here class based

class CarDetailView(ListView):
    """
    This class is done for viewing details of the car in index2.html.
    Alongside viewing, also deals with the filter of the car details through date.
    
    parameters: ListView
    
    returns:
    1. queryset(containing details of car details) 
    2. context(to render wing details for the parking wing)
    """
    model = CarDetail
    template_name = 'index2.html'
    context_object_name = 'cars'

    
    def get_queryset(self):
        queryset = super().get_queryset()
        date_filter = self.request.GET.get('date_filter')
        if date_filter:
            queryset = queryset.filter(parkingdetail__vehicle_arrived_date=date_filter)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Fetch parking wing details
        wings = Parking.objects.filter(is_available=True)
        
        # Add parking wing details to the context
        context['wings'] = wings
        
        return context

    

class CarDetailMoreView(DetailView):
    """
    This class is done for viewing more details of the car in index2.html through  modal consisting 
    of data like car name, owner name and number, parking wing and arrived and left date and time
    
    
    parameters: DetailView
    
    returns:
    1. queryset(containing details of parking details) 
    
    """
    model = ParkingDetail
    template_name = 'index2.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        car_id = self.request.POST.get('car_id')
        


        queryset = queryset.filter(parkingdetail__id=car_id)
        return queryset    
    
    
    
class OwnerProfileView(DetailView):
    """
    This class is responsible for viewing the owner details with help of the model OwnerProfile
    showing data like owner name, number, address, gender and vehicle owned
    
    parameters: DetailView
    
    return:
    1. queryset(owner details)
    2. context(car details)
    
    """
    model = OwnerProfile
    template_name = 'index2.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        car_id = self.request.GET.get('car_id')  
        
        car_detail = CarDetail.objects.get(id=car_id)
        
        queryset = queryset.filter(owner_name_profile=car_detail)
        return queryset   
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car_id = self.request.GET.get('car_id')
        car_detail = CarDetail.objects.get(id=car_id)
        context['object'] = car_detail  
        return context
    