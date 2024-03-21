from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class AuthTable(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True, primary_key=True)
    password = models.CharField(max_length=255)
    last_login = None

    USERNAME_FIELD = 'username'

    class Meta:
        db_table = 'AuthTable'
        managed = False
