from django.contrib import messages,auth,sessions
from django.utils import timezone
from django.shortcuts import render,redirect
from .forms import Registrationform
from .models import Account
from django.contrib.auth.decorators import login_required
from users.models import Trip

# Create your views here.


#SignUp
def sign_up(request):
    if 'super_username' not in request.session:
        return redirect('admin_home')
    
    if request.method == 'POST':
        form = Registrationform(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            # Check if the username already exists
            if Account.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists.')
                return redirect('sign_up')

            user = Account.objects.create_user(username=username, password=password)
            user.set_password(password)
            user.is_active = True
            user.save()
            
            return render(request, 'admins_temp/admin-home.html')
        else:
            messages.info(request, 'Both passwords do not match')
    else:
        form = Registrationform()
    
    context = {
        'form': form,
    }
    return render(request, 'accounts_temp/sign-up.html', context)


#Login
def login_user(request):
    if 'super_username' in request.session:
        return redirect('admin_home')
    
    if 'username' in request.session:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user=auth.authenticate(username=username,password=password)
        if user is not None and user.is_superadmin:
            request.session['super_username'] = username
            auth.login(request,user)
            return redirect('admin_home')
        
        elif user is not None:
            request.session['username'] = username
            auth.login(request,user)
            return redirect('home')

        else:
            messages.error(request,'Invalid login credentials')
            return redirect('login_user')
    return render(request, 'accounts_temp/login.html')


#Logout
@login_required(login_url='login_user')
def logout_user(request):
    user = request.user

    if not user.is_admin:
        current_time_utc = timezone.now()
        today_date = timezone.localtime(current_time_utc).date()

        try:
            user_trip_status = Trip.objects.get(route=request.user, date=today_date, status='Active')
            user_trip_status.status = 'Completed'
            user_trip_status.save()
        except Trip.DoesNotExist:
            pass

    auth.logout(request)
    return redirect('login_user')