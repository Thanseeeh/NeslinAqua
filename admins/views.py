from django.shortcuts import render, redirect
from accounts.models import Account

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
    if 'q' in request.GET:
        q = request.GET['q']
        data = Account.objects.filter(username__icontains=q)
    else:
        data = Account.objects.all().order_by('id')

    context = {'data': data}
    return render(request, 'admins_temp/admin-users.html', context)


# Admin Transactions
def admin_transactions(request):
    return render(request, 'admins_temp/admin-transactions.html')


#Block user
def block_user(request, user_id):
    user = Account.objects.get(id=user_id)
    user.is_active = False
    user.save()
    return redirect('admin_users')


#UnBlock user
def unblock_user(request, user_id):
    user = Account.objects.get(id=user_id)
    user.is_active = True
    user.save()
    return redirect('admin_users')