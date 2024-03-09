"""
Models for Users
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):
    """
    Model class for users
    """

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "balance"]  # for making superuser enter additional required field

    email = models.EmailField(
        unique=True,
        error_messages={
            "unique": ("A user with that email already exists."),
        },
    )
    username = models.CharField(max_length=20)
    city = models.CharField(max_length=20, blank=True)
    state = models.CharField(max_length=20, blank=True)
    zipcode = models.CharField(max_length=8, blank=True)
    balance = models.DecimalField(max_digits=9, decimal_places=2, default=1000)
    is_restaurant_owner = models.BooleanField(default=False)

    def delete(self):
        self.is_active = False
        self.restaurants.filter(is_active=True).update(is_active=False)
        self.save()
