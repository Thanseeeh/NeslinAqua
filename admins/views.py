from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from accounts.models import Account
from accounts.forms import Registrationform
from users.models import Trip, Sales, Payments, Store
from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import calendar
from datetime import datetime
from django.http import JsonResponse

# Create your views here.


# Admin Home
def admin_home(request):
    if 'super_username' not in request.session:
        return redirect('login_user') 
    
    sale = Sales.objects.all()
    expence = Payments.objects.all()

    total_sale = sale.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expence = expence.aggregate(Sum('amount'))['amount__sum'] or 0
    total_revenue = total_sale - total_expence

    # Get distinct years from the Sales table
    available_years_query = Sales.objects.dates('date', 'year').order_by('-date__year').distinct()
    # Extract only the year from each date in the QuerySet
    available_years = [year.year for year in available_years_query]
    
    yearly_data = []
    for year in available_years:
        sales = Sales.objects.filter(
            date__year=year
        )
        expenses = Payments.objects.filter(
            date__year=year
        )

        total_sales_amount = sales.aggregate(Sum('amount'))['amount__sum'] or 0
        total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        total_revenue = total_sales_amount - total_expenses

        yearly_data.append({
            'year': year,
            'total_sales_amount': total_sales_amount,
            'total_expenses': total_expenses,
            'total_revenue': total_revenue,
        })

    current_time_utc = timezone.now()
    current_day = timezone.localtime(current_time_utc).date()
    today_sale = Sales.objects.filter(date=current_day)
    today_expence = Payments.objects.filter(date=current_day)

    today_sales_amount = today_sale.aggregate(Sum('amount'))['amount__sum'] or 0
    today_expenses = today_expence.aggregate(Sum('amount'))['amount__sum'] or 0
    today_revenue = today_sales_amount - today_expenses

    routes = Account.objects.filter(is_admin=False)
    trips = Trip.objects.filter(date=current_day, status='Active')

    stores_details = []
    for route in routes:
        stores = Store.objects.filter(route=route)
        route_sale = Sales.objects.filter(route=route)
        jars_count = route_sale.aggregate(Sum('jars'))['jars__sum'] or 0
        route_revune = route_sale.aggregate(Sum('amount'))['amount__sum'] or 0

        stores_details.append({
            'route': route,
            'store_count': stores.count(),
            'jars_count': jars_count,
            'route_revune': route_revune,
        })

    context = {
        'total_sale': total_sale,
        'total_expence': total_expence,
        'total_revenue': total_revenue,
        'yearly_data': yearly_data,
        'today_sales_amount': today_sales_amount,
        'today_expenses': today_expenses,
        'today_revenue': today_revenue,
        'routes': routes,
        'trips': trips,
        'stores_details': stores_details,
    }
    return render(request, 'admins_temp/admin-home.html', context)


# Admin Profile
def admin_profile(request):
    return render(request, 'admins_temp/admin-profile.html')


# Admin Routes
def admin_routes(request):
    current_time_utc = timezone.now()
    current_day = timezone.localtime(current_time_utc).date()
    routes = Account.objects.filter(is_admin=False)
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


# Route Details
def route_details(request, route):
    route = route
    route_object = Account.objects.filter(id=route).first()
    current_time_utc = timezone.now()
    current_day = timezone.localtime(current_time_utc).date()

    stores = Store.objects.filter(route=route)
    store_sales = []
    for store in stores:
        sales_records = Sales.objects.filter(store=store, route=route, date=current_day).order_by('-date')
        store_sales.append({'store': store, 'sales_records': sales_records})
    
    expences = Payments.objects.filter(route=route, date=current_day)

    context = {
        'route_object': route_object,
        'stores': stores,
        'store_sales': store_sales,
        'expences': expences,
    }
    return render(request, 'admins_temp/route_details.html', context)


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
    transactions = Sales.objects.all().order_by('-date')[:5]

    # Get distinct years from the Sales table
    available_years_query = Sales.objects.dates('date', 'year').order_by('-date__year').distinct()

    # Extract only the year from each date in the QuerySet
    available_years = [year.year for year in available_years_query]

    # Default values for the current month
    selected_year = request.GET.get('selected_year', datetime.now().year)
    selected_month = request.GET.get('selected_month', datetime.now().strftime('%B').lower())

    # Map month names to their corresponding numbers (using lowercase keys)
    month_dict = {v.lower(): k for k, v in enumerate(calendar.month_name) if v}

    # Convert month name to number
    selected_month_number = month_dict[selected_month.lower()]

    months = list(calendar.month_name)[1:]
    routes = Account.objects.filter(is_admin=False)
    route_details = []

    for route in routes:
        sales = Sales.objects.filter(
            route=route,
            date__month=selected_month_number,
            date__year=selected_year
        )
        expenses = Payments.objects.filter(
            route=route,
            date__month=selected_month_number,
            date__year=selected_year
        )

        total_sales_amount = sales.aggregate(Sum('amount'))['amount__sum'] or 0
        total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        total_revenue = total_sales_amount - total_expenses

        route_details.append({
            'route': route,
            'total_sales_amount': total_sales_amount,
            'total_expenses': total_expenses,
            'total_revenue': total_revenue,
        })

    summery = []
    summery_income = Sales.objects.filter(date__month=selected_month_number, date__year=selected_year)
    summery_exenses = Payments.objects.filter(date__month=selected_month_number, date__year=selected_year)

    total_summery_income = summery_income.aggregate(Sum('amount'))['amount__sum'] or 0
    total_summery_exenses = summery_exenses.aggregate(Sum('amount'))['amount__sum'] or 0
    total_summery_net_income = total_summery_income - total_summery_exenses

    context = {
        'transactions': transactions,
        'current_month': selected_month.capitalize(),
        'months': months,
        'route_details': route_details,
        'available_years': available_years,
        'selected_year': int(selected_year),
        'selected_month': selected_month,
        'total_summery_income': total_summery_income,
        'total_summery_exenses': total_summery_exenses,
        'total_summery_net_income': total_summery_net_income,
    }
    return render(request, 'admins_temp/admin-transactions.html', context)


# Admin Old Balances
def admin_old_balances(request):
    accounts = Account.objects.all()
    context = {'accounts': accounts}
    return render(request, 'admins_temp/admin-old-balances.html', context)


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


# Transaction Listing
def transaction_listing(request):
    transactions = Sales.objects.all().order_by('-date')

    transactions_per_page = 10
    page = request.GET.get('page', 1)
    paginator = Paginator(transactions, transactions_per_page)

    try:
        transactions_page = paginator.page(page)
    except PageNotAnInteger:
        transactions_page = paginator.page(1)
    except EmptyPage:
        transactions_page = paginator.page(paginator.num_pages)

    context = {
        'transactions_page': transactions_page,
    }

    return render(request, 'admins_temp/transaction-listing.html', context)