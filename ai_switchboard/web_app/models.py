from django.db import models
from django.contrib.auth.models import AbstractBaseUser


# Define a custom user model named AuthTable
class AuthTable(AbstractBaseUser):
    # Define a username field. This field is unique and used as the primary key.
    username = models.CharField(max_length=255, unique=True, primary_key=True)
    # Define a password field.
    password = models.CharField(max_length=255)
    # Define a last_login field. This field is not used in this model.
    last_login = None

    # Specify the field that will be used as the username field.
    USERNAME_FIELD = 'username'

    class Meta:
        # Specify the name of the database table.
        db_table = 'AuthTable'
        # Specify that Django should not create and manage the database table.
        managed = False
