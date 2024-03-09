"""
Custom permissions for Users
"""

from rest_framework import permissions


class IsLoggedInUser(permissions.BasePermission):
    """
    Custom permission to only allow logged in user to view or edit their details
    and anyone to register.
    """

    def has_permission(self, request, view):
        if request.method == "POST":
            return True

        return request.user.is_authenticated
