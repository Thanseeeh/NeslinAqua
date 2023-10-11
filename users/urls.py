from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user-payments/', views.payments, name='payments'),
    path('user-profile/', views.profile, name='profile'),
    path('add-store/', views.add_store, name='add_store'),
    path('add-sale/<int:store_id>/', views.add_sale, name='add_sale'),
]