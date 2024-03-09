"""
Custom permissions for Users
"""

from rest_framework import permissions


class IsPostRequest(permissions.BasePermission):
    """
    Custom permission to allow if request method is post
    """

    def has_permission(self, request, _view) -> bool:
        """
        Function to check if request if post

        Args:
            request: Request object

        Returns:
            bool: `True` if permission is granted, `False` otherwise.
        """

        return request.method == "POST"
