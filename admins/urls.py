from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_home, name='admin_home'),
    path('admin-profile/', views.admin_profile, name='admin_profile'),
    path('admin-routes/', views.admin_routes, name='admin_routes'),
    path('admin-users/', views.admin_users, name='admin_users'),
    path('admin-transactions/', views.admin_transactions, name='admin_transactions'),
    path('block_user/<int:user_id>/', views.block_user, name='block_user'),
    path('unblock_user/<int:user_id>/', views.unblock_user, name='unblock_user'),
]