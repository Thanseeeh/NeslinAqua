from django.db import models
from accounts.models import Account

# Create your models here.


# AddStore
class Store(models.Model):
    name            = models.CharField(max_length=200, null=True)
    price_for_jar   = models.FloatField()
    stand           = models.IntegerField(blank=True, null=True, default=0)
    dispencer       = models.IntegerField(blank=True, null=True, default=0)
    route           = models.ForeignKey(Account, on_delete=models.CASCADE)
    is_active       = models.BooleanField(default=True)
    created_date    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

# Dashboard Status
class DashboardStatus(models.Model):
    is_active = models.BooleanField(default=False)