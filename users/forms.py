from django import forms
from .models import Store

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'price_for_jar', 'stand', 'dispencer', 'jar']
        widgets = {
            'name'          : forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Name'}),
            'price_for_jar' : forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': '0.00'}),
            'stand'         : forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': '0'}),
            'dispencer'     : forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': '0'}),
            'jar'           : forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': '0'}),
        }