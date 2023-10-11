from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from .models import DashboardStatus, Store, Sales
from .forms import StoreForm, TripForm, SalesForm

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

    stores = Store.objects.filter(route=request.user)

    store_sales = []
    for store in stores:
        current_day = timezone.now().date()
        sales_records = Sales.objects.filter(store=store, date__date=current_day).order_by('-date')
        store_sales.append({'store': store, 'sales_records': sales_records})

    context = {
        'dashboard_status': dashboard_status,
        'trip_form': trip_form,
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
    if request.method == 'POST':
        form = SalesForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.store = store
            sale.route = request.user
            sale.jars = int(sale.jars)
            sale.amount = sale.jars * store.price_for_jar
            sale.is_delivered = True
            sale.save()
            return redirect('home')
    else:
        form = SalesForm()

    context = {'form': form, 'store': store}
    return render(request, 'users_temp/sale.html', context)