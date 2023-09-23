from django import forms
from .models import Route


# Route Form
class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Route Name', 'style': 'height: 2.8em; border-radius: 10px;'}),
        }