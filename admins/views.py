from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from accounts.models import Account
from accounts.forms import Registrationform
from users.models import Trip, Sales, Payments, Store, CreditDebitAmounts
from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import calendar
from datetime import datetime
from django.http import JsonResponse
from users.forms import SalesForm
from decimal import Decimal
from django.db.models import F

# Create your views here.


# Admin Home
def admin_home(request):
    if 'super_username' not in request.session:
        return redirect('login_user') 
    
    sale = Sales.objects.all()
    expence = Payments.objects.all()
    old_balance = Store.objects.all()

    total_sale = sale.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expence = expence.aggregate(Sum('amount'))['amount__sum'] or 0
    total_old_balance = old_balance.aggregate(Sum('old_balance'))['old_balance__sum'] or 0
    total_revenue = total_sale - total_expence - total_old_balance

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
        total_expense_amount = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        total_revenue_amount = total_sales_amount - total_expense_amount

        yearly_data.append({
            'year': year,
            'total_sales_amount': total_sales_amount,
            'total_expense_amount': total_expense_amount,
            'total_revenue_amount': total_revenue_amount,
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
        'total_old_balance': total_old_balance,
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


# Admin Routes
def admin_routes(request):
    current_time_utc = timezone.now()
    today = timezone.localtime(current_time_utc).date()

    selected_date = today

    if request.method == 'GET' and 'selected_date' in request.GET:
        selected_date_str = request.GET.get('selected_date')
        selected_date = timezone.datetime.strptime(selected_date_str, '%Y-%m-%d').date()

    routes = Account.objects.filter(is_admin=False)
    trip = Trip.objects.filter(date=selected_date, status='Active')

    route_details = []

    for route in routes:
        trips = Trip.objects.filter(route=route, date=selected_date)
        sales = Sales.objects.filter(route=route, date=selected_date)
        expenses = Payments.objects.filter(route=route, date=selected_date)
        new_credit = CreditDebitAmounts.objects.filter(route=route, date=selected_date, title='Pending')
        received_oldbalance = CreditDebitAmounts.objects.filter(route=route, date=selected_date, title='Received')
        google_pay = CreditDebitAmounts.objects.filter(route=route, date=selected_date, title='GooglePay')

        total_jars_sold = trips.aggregate(Sum('jars_sold'))['jars_sold__sum'] or 0
        total_jars = trips.aggregate(Sum('jars'))['jars__sum'] or 0
        total_sales_amount = sales.aggregate(Sum('amount'))['amount__sum'] or 0
        total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        new_credit_amount = new_credit.aggregate(Sum('amount'))['amount__sum'] or 0
        new_received_oldbalance = received_oldbalance.aggregate(Sum('amount'))['amount__sum'] or 0
        google_pay_amount = google_pay.aggregate(Sum('amount'))['amount__sum'] or 0
        total_revenue = total_sales_amount - total_expenses + new_received_oldbalance - new_credit_amount
        cash_in_hand = total_revenue - google_pay_amount

        route_details.append({
            'route': route,
            'total_jars_sold': total_jars_sold,
            'total_jars': total_jars,
            'total_sales_amount': total_sales_amount,
            'total_expenses': total_expenses,
            'new_credit_amount': new_credit_amount,
            'new_received_oldbalance': new_received_oldbalance,
            'google_pay_amount': google_pay_amount,
            'cash_in_hand': cash_in_hand,
            'total_revenue': total_revenue,
        })

    #Total Summery Part   
    summery_route_details = []

    summery_sales = Sales.objects.filter(date=selected_date)
    summery_expenses = Payments.objects.filter(date=selected_date)
    summery_new_credit = CreditDebitAmounts.objects.filter(date=selected_date, title='Pending')
    summery_received_oldbalance = CreditDebitAmounts.objects.filter(date=selected_date, title='Received')
    summery_google_pay = CreditDebitAmounts.objects.filter(date=selected_date, title='GooglePay')

    summery_total_sales_amount = summery_sales.aggregate(Sum('amount'))['amount__sum'] or 0
    summery_total_expenses = summery_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    summery_new_credit_amount = summery_new_credit.aggregate(Sum('amount'))['amount__sum'] or 0
    summery_new_received_oldbalance = summery_received_oldbalance.aggregate(Sum('amount'))['amount__sum'] or 0
    summery_google_pay_amount = summery_google_pay.aggregate(Sum('amount'))['amount__sum'] or 0
    summery_total_revenue = summery_total_sales_amount - summery_total_expenses + summery_new_received_oldbalance - summery_new_credit_amount
    summery_cash_in_hand = summery_total_revenue - summery_google_pay_amount
    
    context = {
        'route_details': route_details,
        'trip': trip,
        'today': today,
        'selected_date': selected_date,

        'summery_total_sales_amount': summery_total_sales_amount,
        'summery_total_expenses': summery_total_expenses,
        'summery_new_credit_amount': summery_new_credit_amount,
        'summery_new_received_oldbalance': summery_new_received_oldbalance,
        'summery_google_pay_amount': summery_google_pay_amount,
        'summery_cash_in_hand': summery_cash_in_hand,
        'summery_total_revenue': summery_total_revenue,
    }
    return render(request, 'admins_temp/admin-routes.html', context)


# Route Details
def route_details(request, route):
    selected_date_str = request.GET.get('selected_date')
    if selected_date_str:
        try:
            selected_date = datetime.strptime(selected_date_str, '%b. %d, %Y').date()
        except ValueError:
            selected_date = datetime.strptime(selected_date_str, '%B %d, %Y').date()
    else:
        current_time_utc = timezone.now()
        selected_date = timezone.localtime(current_time_utc).date()

    route = route
    route_object = Account.objects.filter(id=route).first()
    current_day = selected_date

    stores = Store.objects.filter(route=route).order_by('name')
    store_sales = []
    total_jars = 0
    total_amount = 0

    for store in stores:
        sales_records = Sales.objects.filter(store=store, route=route, date=current_day).order_by('-date')
        jars_sum = sales_records.aggregate(Sum('jars'))['jars__sum'] or 0
        amount_sum = sales_records.aggregate(Sum('amount'))['amount__sum'] or 0
        total_jars += jars_sum
        total_amount += amount_sum
        store_sales.append({'store': store, 'sales_records': sales_records})
    
    expences = Payments.objects.filter(route=route, date=current_day)
    credit_debit = CreditDebitAmounts.objects.filter(route=route, date=current_day)

    context = {
        'route_object': route_object,
        'stores': stores,
        'store_sales': store_sales,
        'expences': expences,
        'credit_debit': credit_debit,
        'selected_date': selected_date.strftime('%d-%m-%Y'),
        'total_jars': total_jars,
        'total_amount': total_amount,
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
    accounts = Account.objects.filter(is_admin=False)
    context = {'accounts': accounts}
    return render(request, 'admins_temp/admin-old-balances.html', context)


# Admin Old Balances Single View
def admin_old_balances_single_view(request, route_id):
    account = Account.objects.get(id=route_id)
    sorted_stores = account.store_set.all().order_by('name')

    total_oldbalance = sum(store.old_balance for store in sorted_stores)
    account.total_oldbalance = total_oldbalance

    context = {'account': account, 'sorted_stores': sorted_stores}
    return render(request, 'admins_temp/admin-old-balances-single-view.html', context)


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


# Edit Jar
def edit_jar(request, record_id):
    sale = Sales.objects.get(id=record_id)
    try:
        trip = Trip.objects.get(route=sale.route, date=sale.date, status='Active')
    except:
        trip = Trip.objects.filter(route=sale.route, date=sale.date).last()   
    old_jars = sale.jars
    form = SalesForm(instance=sale)

    if request.method == 'POST':
        form = SalesForm(request.POST, instance=sale)
        if form.is_valid():
            jars = form.cleaned_data['jars']

            # Convert float to Decimal for precise arithmetic
            store_price = Decimal(str(sale.store.price_for_jar))

            # Calculate the new amount based on the updated jar count
            sale.amount = jars * store_price

            # Determine the difference between the old jar count and the new one
            jars_difference = jars - old_jars

            # Update the jars_sold count by adding the difference to the current value
            trip.jars_sold += jars_difference

            # Update the sale object with the new jar count and amount
            sale.jars = jars
            trip.save()
            sale.save()

            return redirect('admin_routes')

    context = {'sale': sale, 'form': form}
    return render(request, 'admins_temp/edit-jar.html', context