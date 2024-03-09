"""
Models for Users
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):
    """
    Model class for users
    """

    email = models.EmailField(unique=True)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    zipcode = models.CharField(max_length=20)
    balance = models.FloatField(default=1000)
