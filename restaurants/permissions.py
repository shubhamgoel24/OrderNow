"""
Custom permissions for Restaurants
"""

from rest_framework import permissions

from restaurants.models import Restaurants


class ReadOnlyPermission(permissions.BasePermission):
    """
    Custom permission to allow anyone to fetch restaurant or menu details.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return False


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owner of restaurant to update details.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsRestaurantOwner(permissions.BasePermission):
    """
    Custom permission to only allow owner of restaurant to update menu or fetch orders list.
    """

    def has_permission(self, request, view):
        restaurant_id = view.kwargs["restaurant_id"]
        try:
            restaurant = Restaurants.objects.get(pk=restaurant_id)
        except Restaurants.DoesNotExist:
            return False
        return restaurant.is_active and restaurant.owner == request.user


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
