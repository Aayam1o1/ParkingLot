from django.shortcuts import render, redirect, get_object_or_404
from .forms import addVehicleForm, parkingWingForm, editVehicleForm
from .models import *

def index(request):

    cars = CarDetail.objects.all()
    wings = Parking.objects.filter(isAvailable=True)

    context = {
        'cars': cars,
        'wings': wings,

    }
    return render(request, 'index.html', context)


def parking(request):
    if request.method == "POST":
        form = parkingWingForm(request.POST)
        
        if form.is_valid():
            
            form.save()
            return redirect('/')

    else:
        form = parkingWingForm()

    return render(request, 'parking.html', {'form': form})

def car(request):
    if request.method == "POST":
        form = addVehicleForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('/')

    else:
        form = addVehicleForm()

    return render(request, 'car.html', {'form': form})


def edit_car(request):
    if request.method == "POST":
        car_id = request.POST.get('car_id')
        car = get_object_or_404(CarDetail, id=car_id)
        form = editVehicleForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            return redirect('/')  # Redirect after successful form submission
        else:
            print(form.errors)
            wings = Parking.objects.filter(isAvailable=True)
            cars = CarDetail.objects.all()
            context = {
                'cars': cars,
                'wings': wings,
                'form': form,
                'car': car,
            }
            return render(request, 'index.html', context)
    return redirect('/')

def delete_car(request):
    if request.method == "POST":
        car_id = request.POST.get('car_id')
        car = get_object_or_404(CarDetail, id=car_id)
        car.delete()

    
    return redirect('/')
