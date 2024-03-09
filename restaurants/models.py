"""
Models for Restaurants
"""

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
