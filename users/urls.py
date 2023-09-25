from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user-profile/', views.profile, name='profile'),
    path('add-store/', views.add_store, name='add_store'),
]