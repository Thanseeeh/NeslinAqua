from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from accounts.models import Account
from accounts.forms import Registrationform
from users.models import Trip, Sales, Payments
from django.db.models import Sum

# Create your views here.


# Admin Home
def admin_home(request):
    if 'super_username' not in  request.session:
        return redirect('login_user') 
    return render(request, 'admins_temp/admin-home.html')


# Admin Profile
def admin_profile(request):
    return render(request, 'admins_temp/admin-profile.html')


# Admin Routes
def admin_routes(request):
    current_time_utc = timezone.now()
    current_day = timezone.localtime(current_time_utc).date()
    routes = Account.objects.all()
    trip = Trip.objects.filter(date=current_day, status='Active')

    route_details = []

    for route in routes:
        trips = Trip.objects.filter(route=route, date=current_day)
        sales = Sales.objects.filter(route=route, date=current_day)
        expenses = Payments.objects.filter(route=route, date=current_day)

        total_jars_sold = trips.aggregate(Sum('jars_sold'))['jars_sold__sum'] or 0
        total_jars = trips.aggregate(Sum('jars'))['jars__sum'] or 0
        total_sales_amount = sales.aggregate(Sum('amount'))['amount__sum'] or 0
        total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        total_revenue = total_sales_amount - total_expenses

        route_details.append({
            'route': route,
            'total_jars_sold': total_jars_sold,
            'total_jars': total_jars,
            'total_sales_amount': total_sales_amount,
            'total_expenses': total_expenses,
            'total_revenue': total_revenue,
        })

    context = {
        'route_details': route_details,
        'trip': trip,
    }
    return render(request, 'admins_temp/admin-routes.html', context)


# Admin Users
def admin_users(request):
    if 'q' in request.GET:
        q = request.GET['q']
        data = Account.objects.filter(username__icontains=q)
    else:
        data = Account.objects.filter(is_admin=False).order_by('id')

    context = {'data': data}
    return render(request, 'admins_temp/admin-users.html', context)


# Admin Transactions
def admin_transactions(request):
    return render(request, 'admins_temp/admin-transactions.html')


# Block user
def block_user(request, user_id):
    user = Account.objects.get(id=user_id)
    user.is_active = False
    user.save()
    return redirect('admin_users')


# UnBlock user
def unblock_user(request, user_id):
    user = Account.objects.get(id=user_id)
    user.is_active = True
    user.save()
    return redirect('admin_users')


# Edit Users
def edit_user(request, user_id):
    user = Account.objects.get(id=user_id)
    form = Registrationform(instance=user)

    if request.method == 'POST':
        form = Registrationform(request.POST, instance=user)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user.set_password(password)
            user.is_active = True
            user.save()
            return redirect('admin_users')

    context = {'user': user, 'form': form}
    return render(request, 'admins_temp/edit-user.html', context)