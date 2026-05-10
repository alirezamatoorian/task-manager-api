from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import UserManager


# Create your models here.


class Users(AbstractBaseUser, PermissionsMixin):
    pass
