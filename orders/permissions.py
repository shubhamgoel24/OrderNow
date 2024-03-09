"""
Custom permissions for Orders
"""

from rest_framework import permissions

from restaurants.models import Restaurants


class IsRestaurantActive(permissions.BasePermission):
    """
    Custom permission to only allow orders for active restaurants.
    """

    def has_permission(self, request, view):
        restaurant_id = view.kwargs["restaurant_id"]
        try:
            restaurant = Restaurants.objects.get(pk=restaurant_id)
        except Restaurants.DoesNotExist:
            return False
        return restaurant.is_active
