import uuid
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
    )
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, username, email, first_name, last_name, password=None, **extra_fields):
        if not username:
            raise ValueError("User must have a username")
        if not email:
            raise ValueError("User must have a email")

        user = self.model(username=username, email=self.normalize_email(email), first_name=first_name, last_name=last_name, **extra_fields)

        user.set_password(password) #Hashing password

        user.save()
        return user

    def create_superuser(self, username, email, first_name, last_name, password=None, **extra_fields):
        if not username:
            raise ValueError("User must have a username")
        if not email:
            raise ValueError("User must have a email")

        superuser = self.model(username=username, email=self.normalize_email(email), first_name=first_name, last_name=last_name, **extra_fields)

        superuser.is_superuser = True
        superuser.is_staff = True
        superuser.set_password(password)

        superuser.save()
        return superuser

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) #Access to the django admin site
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def token(self):
        refresh_token = RefreshToken.for_user(self)

        return {
            'refresh': str(refresh_token),
            'access': str(refresh_token.access_token)
        }