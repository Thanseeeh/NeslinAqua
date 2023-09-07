from django.shortcuts import render, redirect

# Create your views here.


#Home
def home(request):
    if 'username' not in  request.session:
        return redirect('login_user') 
    return render(request, 'users_temp/index.html')