from django.db import models
from accounts.models import Account

# Create your models here.


# AddStore
class Store(models.Model):
    name            = models.CharField(max_length=200, null=True)
    price_for_jar   = models.FloatField()
    stand           = models.IntegerField(blank=True, null=True, default=0)
    dispencer       = models.IntegerField(blank=True, null=True, default=0)
    jar             = models.IntegerField(blank=True, null=True, default=0)
    route           = models.ForeignKey(Account, on_delete=models.CASCADE)
    is_active       = models.BooleanField(default=True)

    def __str__(self):
        return self.name