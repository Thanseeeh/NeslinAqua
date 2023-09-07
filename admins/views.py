from django.shortcuts import render, redirect

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
    return render(request, 'admins_temp/admin-routes.html')


# Admin Users
def admin_users(request):
    return render(request, 'admins_temp/admin-users.html')


# Admin Transactions
def admin_transactions(request):
    return render(request, 'admins_temp/admin-transactions.html')