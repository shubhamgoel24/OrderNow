"""
Custom permissions for Orders
"""

from rest_framework import permissions


class IsOwnerOrCustomer(permissions.BasePermission):
    """
    Custom permission to only allow owner of restaurant or customer to update order.
    """

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Function to check if user has permission for orders object
        """

        return obj.customer == request.user or obj.restaurant.owner == request.user
