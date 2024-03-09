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


class Orders(models.Model):
    """
    Model class for orders
    """

    class OrderStatuses(models.TextChoices):
        IN_PROGRESS = "In Progress"
        DISPATCHED = "Dispatched"
        DELIVERED = "Delivered"
        CANCELLED = "Cancelled"

    status = models.CharField(max_length=12, choices=OrderStatuses.choices, default=OrderStatuses.IN_PROGRESS)
    restaurant = models.ForeignKey(Restaurants, related_name="orders", on_delete=models.PROTECT)
    customer = models.ForeignKey(Users, related_name="orders", on_delete=models.PROTECT)
    order_datetime = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=9, decimal_places=2)
    address = models.CharField(max_length=256)
    contact = models.CharField(max_length=10)


class OrderItems(models.Model):
    """
    Model class for order items
    """

    item = models.ForeignKey(Menus, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.PositiveIntegerField()
    order = models.ForeignKey(Orders, related_name="items", on_delete=models.PROTECT)
