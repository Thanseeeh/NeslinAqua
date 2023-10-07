from celery import shared_task
from django.contrib.auth import logout
from .models import Account

@shared_task
def logout_users():
    # Logout all active users
    for user in Account.objects.filter(is_active=True):
        logout(user)
