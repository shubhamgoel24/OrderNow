"""
Models for Orders
"""

from django.db import models

from restaurants.models import Menus, Restaurants
from users.models import Users


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
