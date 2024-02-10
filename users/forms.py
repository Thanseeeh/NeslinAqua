from django import forms
from .models import Store, Trip, Sales, Payments


class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'price_for_jar']
        # fields = ['name', 'price_for_jar', 'stand', 'dispencer']
        widgets = {
            'name'          : forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Name'}),
            'price_for_jar' : forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': '0.00'}),
            # 'stand'         : forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': '0'}),
            # 'dispencer'     : forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': '0'}),
        }


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['jars']
        widgets = { 'jars' : forms.NumberInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Number of Jars', 'step': 1})}


class SalesForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = ['jars']
        widgets = { 'jars' : forms.NumberInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Number of Jars', 'step': 1})}


class ExpenceForm(forms.ModelForm):
    class Meta:
        model = Payments
        fields = ['title', 'amount']
        widgets = {
            'title'          : forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Title'}),
            'amount' : forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': '0.00'}),
        }


class OldBalanceForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['old_balance']
        widgets = {
            'old_balance' : forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': '0.00'}),
        }