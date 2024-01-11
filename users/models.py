from django.db import models
from accounts.models import Account

# Create your models here.


# Add Store
class Store(models.Model):
    name            = models.CharField(max_length=200, null=True)
    price_for_jar   = models.FloatField()
    stand           = models.IntegerField(blank=True, null=True, default=0)
    dispencer       = models.IntegerField(blank=True, null=True, default=0)
    route           = models.ForeignKey(Account, on_delete=models.CASCADE)
    is_active       = models.BooleanField(default=True)
    created_date    = models.DateField(auto_now_add=True)
    old_balance     = models.IntegerField(default=0)

    def __str__(self):
        return self.name


# Daily Trip
class Trip(models.Model):
    jars    = models.PositiveIntegerField(default=0)
    jars_sold = models.PositiveIntegerField(default=0)
    date    = models.DateField(auto_now_add=True)
    route   = models.ForeignKey(Account, on_delete=models.CASCADE)
    status  = models.CharField(max_length=20, default='Active')


# Shop Sales
class Sales(models.Model):
    jars    = models.PositiveIntegerField(default=0)
    store   = models.ForeignKey(Store, on_delete=models.CASCADE)
    date    = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    route   = models.ForeignKey(Account, on_delete=models.CASCADE)
    is_delivered = models.BooleanField(default=False)


# Daily Payments
class Payments(models.Model):
    title   = models.CharField(max_length=100, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date    = models.DateField(auto_now_add=True)
    route   = models.ForeignKey(Account, on_delete=models.CASCADE)
