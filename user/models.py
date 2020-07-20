import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email...!')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.activation_code = uuid.uuid4()
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.activation_code = None

        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False, blank=False)
    name = models.CharField(max_length=255, null=True)
    address = models.TextField(null=True)
    postal_code = models.CharField(max_length=10, null=True)
    national_code = models.CharField(max_length=10, null=True, unique=True)
    activation_code = models.CharField(default=None, max_length=255, null=True)
    phone_number = models.CharField(max_length=13, null=True, unique=True)
    bank_account = models.CharField(max_length=16, null=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
