from django.db import models

# Create your models here.


# Route Model
class Route(models.Model):
    name        = models.CharField(max_length=200, null=True)
    is_active   = models.BooleanField(default=True)

    def __str__(self):
        return self.name