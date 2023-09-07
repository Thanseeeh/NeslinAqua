from django import forms
from .models import Account

#Signup form
class Registrationform(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['username', 'email', 'password', 'confirm_password']

    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Username'})
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Email address'})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Password'})
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Confirm Password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Entered passwords do not match each other!")