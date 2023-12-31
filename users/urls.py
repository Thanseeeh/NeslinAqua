from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user-payments/', views.payments, name='payments'),
    path('user-profile/', views.profile, name='profile'),
    path('add-store/', views.add_store, name='add_store'),
    path('edit-store/<int:store_id>/', views.edit_store, name='edit_store'),
    path('add-sale/<int:store_id>/', views.add_sale, name='add_sale'),
    path('add-expence/', views.add_expence, name='add_expence'),
    path('trip-details/', views.trip_details, name='trip_details'),
]