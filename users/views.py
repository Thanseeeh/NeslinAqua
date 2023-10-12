from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from .models import DashboardStatus, Store, Sales, Trip
from .forms import StoreForm, TripForm, SalesForm

# Create your views here.


# Home
def home(request):
    if 'username' not in request.session:
        return redirect('login_user')

    route = request.user
    dashboard_status = DashboardStatus.objects.first()
    # Check if the route's trip is already started
    current_day = timezone.now().date()
    trip_started = Trip.objects.filter(route=route, date=current_day).exists()

    if request.method == 'POST':
        if trip_started:
            # Handle sale submission
            form = SalesForm(request.POST)
            if form.is_valid():
                sale = form.save(commit=False)
                sale.store.route = route
                sale.route = route
                sale.jars = int(sale.jars)
                sale.amount = sale.jars * sale.store.price_for_jar
                sale.is_delivered = True
                sale.save()

                # Update jars_sold for the current trip
                trip = Trip.objects.get(route=route, date=current_day)
                trip.jars_sold += sale.jars
                trip.save()

                # Check if all jars are sold and log out the route if so
                if trip.jars_sold >= trip.jars:
                    messages.info(request, 'All jars are sold. Logging out.')
                    return redirect('logout_user')
        else:
            # Handle trip start
            trip_form = TripForm(request.POST)
            if trip_form.is_valid():
                trip = trip_form.save(commit=False)
                trip.route = route
                trip.date = current_day  # Set the date to current_day
                trip.save()
                dashboard_status.is_active = True
                dashboard_status.save()
                return redirect('home')
    else:
        trip_form = TripForm()

    stores = Store.objects.filter(route=route)
    store_sales = []

    for store in stores:
        sales_records = Sales.objects.filter(store=store, route=route, date=current_day).order_by('-date')
        store_sales.append({'store': store, 'sales_records': sales_records})

    context = {
        'dashboard_status': dashboard_status,
        'trip_form': trip_form,
        'trip_started': trip_started,
        'store_sales': store_sales,
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


# AddSale
def add_sale(request, store_id):
    store = Store.objects.get(pk=store_id)
    route = request.user
    form = SalesForm()

    if request.method == 'POST':
        form = SalesForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.store = store
            sale.route = route
            sale.jars = int(sale.jars)  # Convert to integer
            sale.amount = sale.jars * store.price_for_jar
            sale.is_delivered = True
            sale.save()

            # Retrieve the existing trip for the day
            current_day = timezone.now().date()
            trip, created = Trip.objects.get_or_create(route=route, date=current_day)

            # Convert the 'jars' and 'jars_sold' fields to integers
            trip.jars = int(trip.jars) if trip.jars else 0
            trip.jars_sold = int(trip.jars_sold) if trip.jars_sold else 0

            # Update jars_sold for the existing trip
            trip.jars_sold = trip.jars_sold + sale.jars
            trip.save()

            # Check if all jars are sold
            if trip.jars_sold >= trip.jars:
                messages.info(request, 'All jars are sold. Logging out.')
                return redirect('logout_user')

            return redirect('home')

    # Render the sale.html page
    context = {'form': form, 'store': store}
    return render(request, 'users_temp/sale.html', context)