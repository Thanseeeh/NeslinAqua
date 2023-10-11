from django.shortcuts import render, redirect
from django.contrib import messages
from .models import DashboardStatus
from .forms import StoreForm, TripForm

# Create your views here.


# Home
def home(request):
    if 'username' not in request.session:
        return redirect('login_user')

    dashboard_status = DashboardStatus.objects.first()

    if request.method == 'POST':
        trip_form = TripForm(request.POST)
        if trip_form.is_valid():
            trip = trip_form.save(commit=False)
            trip.route = request.user
            trip.save()
            dashboard_status.is_active = True
            dashboard_status.save()
            return redirect('home')

    else:
        trip_form = TripForm()

    context = {
        'dashboard_status': dashboard_status,
        'trip_form': trip_form,
    }

    return render(request, 'users_temp/index.html', context)


# Payments
def payments(request):
    return render(request, 'users_temp/payments.html')


# Profile
def profile(request):
    return render(request, 'users_temp/profile.html')


# AddStore
def add_store(request):
    route = request.user
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            store = form.save(commit=False)
            store.route = route
            store.save()
            messages.info(request, 'Store Created Successfully')
            return redirect('home')
    else:
        form = StoreForm()
        context = {'form': form, 'route': route}
    return render(request, 'users_temp/add_store.html', context)