from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('User must have an username')
        
        user = self.model(
            username = username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password):
        user = self.create_user(
            username = username,
            password = password,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
    


class Account(AbstractBaseUser):
    username    = models.CharField(max_length=100, unique=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login  = models.DateTimeField(null=True, blank=True)
    is_admin    = models.BooleanField(default=False)
    is_staff    = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)


    USERNAME_FIELD = 'username'

    objects = MyAccountManager()

    def str(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
    
    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)