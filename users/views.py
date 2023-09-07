from django.shortcuts import render

# Create your views here.


#Home
def home(request):
    return render(request, 'users_temp/index.html')