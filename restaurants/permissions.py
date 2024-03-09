"""
Custom permissions for Restaurants
"""

from rest_framework import permissions

from restaurants.models import Restaurants


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owner of restaurant to update details.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class IsRestaurantOwner(permissions.BasePermission):
    """
    Custom permission to only allow owner of restaurant to update menu.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        restaurant_id = view.kwargs["restaurant_id"]
        restaurant = Restaurants.objects.get(pk=restaurant_id)

        return restaurant.is_active and restaurant.owner == request.user
