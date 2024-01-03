from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from accounts.models import Account
from accounts.forms import Registrationform
from users.models import Trip

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
    current_day = timezone.now().date()
    routes = Account.objects.all()
    trip = Trip.objects.filter(date=current_day, status='Active')
    context = {
        'routes': routes,
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