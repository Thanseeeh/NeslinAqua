from django import forms
from .models import Store, Trip


class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'price_for_jar', 'stand', 'dispencer']
        widgets = {
            'name'          : forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Name'}),
            'price_for_jar' : forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': '0.00'}),
            'stand'         : forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': '0'}),
            'dispencer'     : forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': '0'}),
        }


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['jars']
        widgets = { 'jars' : forms.NumberInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Number of Jars', 'step': 1})}