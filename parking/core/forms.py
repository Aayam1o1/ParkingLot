from django import forms
from .models import CarDetail, Parking, ParkingDetail

class parkingWingForm(forms.ModelForm):
    wing_name = forms.CharField(
        label='Parking Wing Name',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Parking Wing Name', 'class': 'form-control'})
    )
    class Meta:
        model = Parking
        fields = ['wing_name']

class addVehicleForm(forms.ModelForm):
    owner_name = forms.CharField(
        label='Owner Name',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Owner Name', 'class': 'form-control'})
    )
    phone_number = forms.CharField(
        label='Phone Number',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'form-control'})
    )
    vehicle_number = forms.CharField(
        label='Vehicle Number',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Vehicle Number', 'class': 'form-control'})
    )
    vehicle_type = forms.CharField(
        label='Vehicle Type',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Vehicle Type', 'class': 'form-control'})
    )
    parking_wing = forms.ModelChoiceField(
        label='Parking Wing',
        queryset=Parking.objects.filter(is_available=True),  # Filter only available parking wings
        empty_label="Select Parking Wing",  # Optional: Provide an empty label
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = CarDetail
        fields = ['owner_name', 'phone_number', 'vehicle_number', 'vehicle_type', 'parking_wing']



class editVehicleForm(forms.ModelForm):
    owner_name = forms.CharField(
        label='Owner Name',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Owner Name', 'class': 'form-control'})
    )
    phone_number = forms.CharField(
        label='Phone Number',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'form-control'})
    )
    vehicle_number = forms.CharField(
        label='Vehicle Number',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Vehicle Number', 'class': 'form-control'})
    )
    vehicle_type = forms.CharField(
        label='Vehicle Type',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Vehicle Type', 'class': 'form-control'})
    )
    parking_wing = forms.ModelChoiceField(
        label='Parking Wing',
        queryset=Parking.objects.filter(is_available=True),  # Filter only available parking wings
        empty_label="Select Parking Wing",  # Optional: Provide an empty label
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CarDetail
        fields = ['owner_name', 'phone_number', 'vehicle_number', 'vehicle_type', 'parking_wing', 'parking_wing']
