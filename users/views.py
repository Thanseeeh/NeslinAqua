from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StoreForm

# Create your views here.


# Home
def home(request):
    if 'username' not in  request.session:
        return redirect('login_user') 
    return render(request, 'users_temp/index.html')


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