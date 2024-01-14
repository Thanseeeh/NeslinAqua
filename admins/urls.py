from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_home, name='admin_home'),
    path('admin-profile/', views.admin_profile, name='admin_profile'),
    path('admin-routes/', views.admin_routes, name='admin_routes'),
    path('admin-users/', views.admin_users, name='admin_users'),
    path('admin-transactions/', views.admin_transactions, name='admin_transactions'),
    path('admin-old-balances/', views.admin_old_balances, name='admin_old_balances'),
    path('block_user/<int:user_id>/', views.block_user, name='block_user'),
    path('unblock_user/<int:user_id>/', views.unblock_user, name='unblock_user'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('route-details/<int:route>/', views.route_details, name='route_details'),
    path('transaction-listing', views.transaction_listing, name='transaction_listing'),
]