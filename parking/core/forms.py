from django import forms
from .models import CarDetail, Parking

class parkingWingForm(forms.ModelForm):
    wingName = forms.CharField(
        label='Parking Wing Name',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Parking Wing Name', 'class': 'form-control'})
    )
    class Meta:
        model = Parking
        fields = ['wingName']

class addVehicleForm(forms.ModelForm):
    ownerName = forms.CharField(
        label='Owner Name',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Owner Name', 'class': 'form-control'})
    )
    phoneNumber = forms.CharField(
        label='Phone Number',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'form-control'})
    )
    vehicleNumber = forms.CharField(
        label='Vehicle Number',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Vehicle Number', 'class': 'form-control'})
    )
    vehicleType = forms.CharField(
        label='Vehicle Type',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Vehicle Type', 'class': 'form-control'})
    )
    parkingWing = forms.ModelChoiceField(
        label='Parking Wing',
        queryset=Parking.objects.filter(isAvailable=True),  # Filter only available parking wings
        empty_label="Select Parking Wing",  # Optional: Provide an empty label
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CarDetail
        fields = ['ownerName', 'phoneNumber', 'vehicleNumber', 'vehicleType', 'parkingWing']



class editVehicleForm(forms.ModelForm):
    ownerName = forms.CharField(
        label='Owner Name',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Owner Name', 'class': 'form-control'})
    )
    phoneNumber = forms.CharField(
        label='Phone Number',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'form-control'})
    )
    vehicleNumber = forms.CharField(
        label='Vehicle Number',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Vehicle Number', 'class': 'form-control'})
    )
    vehicleType = forms.CharField(
        label='Vehicle Type',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Vehicle Type', 'class': 'form-control'})
    )
    parkingWing = forms.ModelChoiceField(
        label='Parking Wing',
        queryset=Parking.objects.filter(isAvailable=True),  # Filter only available parking wings
        empty_label="Select Parking Wing",  # Optional: Provide an empty label
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CarDetail
        fields = ['ownerName', 'phoneNumber', 'vehicleNumber', 'vehicleType', 'parkingWing']
