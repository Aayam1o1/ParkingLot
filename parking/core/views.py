import sweetify
from django.core.signals import request_finished
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView
from django.http import HttpResponse

from .forms import addVehicleForm, editVehicleForm, parkingWingForm
from .models import *
from django.utils.translation import gettext as _
from django.utils.translation import gettext
from django.utils import translation
from django.conf import settings


def car_detail_view(request):
    """
    This function is used to view the car, parking details in the index or
    home page.

    parameter: request

    return:

    webpage index to render car and wing details

    """
    # output = gettext("Welcome to my site.")

    cars = CarDetail.objects.all()
    wings = Parking.objects.filter(is_available=True)
    parking = ParkingDetail.objects.all()
    context = {
        "cars": cars,
        "wings": wings,
        "parking": parking,
    }
    # return HttpResponse(output)
    return render(request, "index.html", context)


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
            return redirect("/")

    else:
        form = parkingWingForm()

    context = {
        "form": form,
        "wings": wings,
        "parking_details": parking_details,
    }

    return render(request, "parking.html", context)


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
            car_detail = form.save(commit=False)
            parking_wing = form.cleaned_data["parking_wing"]

            # if ParkingDetail.objects.filter(parking_wing=parking_wing, vehicle_left_date__isnull=True).exists():
            #     sweetify.error(request, 'The space is occupied already please choose another parking wing')
            #     return redirect('car_detail_create')
            car_detail.save()
            parking_detail = ParkingDetail.objects.create(
                parking_wing=parking_wing,
                vehicle_arrived_date=timezone.now(),
                vehicle_arrived_time=timezone.now(),
            )
            parking_detail.vehicles.add(car_detail)

            return redirect("/")
    else:
        form = addVehicleForm()

    return render(request, "car.html", {"form": form})


def car_detail_edit(request):
    """
    This function is used edit car details
    This function uses form editVehicleForm consisting of data like owner name, phone number,
    vehicle number, vehicle type and parking wing.

    parameter: request

    return redirect "/"

    """
    if request.method == "POST":
        car_id = request.POST.get("car_id")
        car = get_object_or_404(CarDetail, id=car_id)
        form = editVehicleForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            return redirect("/")
        else:
            wings = Parking.objects.filter(is_available=True)
            cars = CarDetail.objects.all()
            context = {
                "cars": cars,
                "wings": wings,
                "form": form,
                "car": car,
            }
            return render(request, "index.html", context)
    return redirect("/")


def car_detail_checkout(request):
    """
    This function is used to check out the car from the parking lot.
    Helps in setting the car left date and time.

    parmeter: request

    return redirect('/')

    """
    if request.method == "POST":
        car_id = request.POST.get("car_id")
        vehicle = get_object_or_404(CarDetail, id=car_id)

        parking_detail = get_object_or_404(ParkingDetail, vehicles=vehicle)

        if not parking_detail.vehicle_has_left:

            parking_detail.vehicle_has_left = True
            parking_detail.vehicle_left_date = timezone.now()
            parking_detail.vehicle_left_time = timezone.now()
            parking_detail.save()

    return redirect("/")


def car_detail_delete(request):
    """
    This function is used to delete the car from the system

    parameters: request

    return redirect('/')
    """

    if request.method == "POST":
        car_id = request.POST.get("car_id")
        car = get_object_or_404(CarDetail, id=car_id)

        car.delete()

    return redirect("/")


def parking_edit(request):
    """
    This function is used edit parking details
    This function uses form parkingWingForm consisting of data wing_name

    parameter: request

    return redirect "/"

    """
    if request.method == "POST":
        wing_id = request.POST.get("wing_id")
        wing = get_object_or_404(Parking, id=wing_id)
        form = parkingWingForm(request.POST, instance=wing)

        if form.is_valid():
            form.save()
            return redirect("parking")
        else:
            wings = Parking.objects.filter(is_available=True)
            context = {
                "wings": wings,
                "form": form,
                "wing": wing,
            }
            return render(request, "parking.html", context)
    return redirect("/")


def parking_delete(request):
    """
    This function is used to delete the parking wing name from the system

    parameters: request

    return redirect('/')
    """
    if request.method == "POST":
        wing_id = request.POST.get("wing_id")
        wing = get_object_or_404(Parking, id=wing_id)

        wing.delete()

    return redirect("/")


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
    template_name = "index2.html"
    context_object_name = "cars"

    def get_queryset(self):
        print(_("Welcome to our site"))

        queryset = super().get_queryset()
        date_filter = self.request.GET.get("date_filter")
        if date_filter:
            queryset = queryset.filter(parkingdetail__vehicle_arrived_date=date_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Var = ParkingDetail.objects.all().values(
            "id", "vehicle_arrived_date", "vehicle_arrived_time"
        )
        # Fetch parking wing details
        wings = Parking.objects.filter(is_available=True)
        car_detail = ParkingDetail.objects.all().values(
            "vehicles",
            "vehicle_arrived_date",
            "vehicle_arrived_time",
            "parking_wing",
            "vehicle_left_time",
            "vehicle_left_date",
        )

        # Add parking wing details to the context
        context["wings"] = wings
        context["var"] = Var[0]
        context["car_detail"] = car_detail

        # Add translated text
        context["filter_label"] = _("Filter by date")
        context["no_results_message"] = _("No results found.")
        
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
    template_name = "index2.html"
    context_object_name = "parking_detail"

    def get_queryset(self):
        queryset = super().get_queryset()
        car_id = self.request.GET.get("car_id")

        # Filter queryset to retrieve details related to the specific car_id
        if car_id:
            queryset = queryset.filter(vehicles__id=car_id).first()

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
    template_name = "index2.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        car_id = self.request.GET.get("car_id")

        car_detail = CarDetail.objects.get(id=car_id)

        queryset = queryset.filter(owned_car=car_detail)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car_id = self.request.GET.get("car_id")
        # car_detail = CarDetail.objects.get(id=car_id)
        context["object"] = OwnerProfile.objects.get(owned_car__id=car_id)
        return context
    
def set_language(request):
    language = request.POST.get('language')
    if language:
        translation.activate(language)
        response = redirect(request.POST.get('next'))
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
        return response
    return redirect('/')