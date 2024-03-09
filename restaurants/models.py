"""
Models for Restaurants
"""

from django.core.validators import MinValueValidator
from django.db import models

from users.models import Users


class Restaurants(models.Model):
    """
    Model class for restaurants
    """

    name = models.CharField(max_length=120)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(Users, related_name="restaurants", on_delete=models.PROTECT)

    def delete(self):
        self.is_active = False
        self.save()


class Menus(models.Model):
    """
    Model class for menus
    """

    name = models.CharField(max_length=120)
    price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    quantity = models.PositiveIntegerField()
    restaurant = models.ForeignKey(Restaurants, related_name="menu", on_delete=models.PROTECT)
