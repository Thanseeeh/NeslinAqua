from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StoreForm

# Create your views here.


# Home
def home(request):
    if 'username' not in  request.session:
        return redirect('login_user') 
    return render(request, 'users_temp/index.html')


# Payments
def payments(request):
    return render(request, 'users_temp/payments.html')


# Profile
def profile(request):
    return render(request, 'users_temp/profile.html')


