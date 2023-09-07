from django.contrib import messages,auth,sessions
from django.shortcuts import render,redirect
from .forms import Registrationform
from .models import Account
from django.contrib.auth.decorators import login_required

# vertification email and reset password
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.views.decorators.cache import cache_control
import re, random
from datetime import datetime, timedelta
from django.utils import timezone

# Create your views here.


#SignUp
def sign_up(request):
    if 'super_username' not in request.session:
        return redirect('admin_home')
    
    if request.method == 'POST':
        form = Registrationform(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            # Check if the username already exists
            if Account.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists.')
                return redirect('sign_up')

            user = Account.objects.create_user(email=email, username=username, password=password)
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
        if user is not None and user.is_superuser:
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
    auth.logout(request)
    return redirect('login_user')