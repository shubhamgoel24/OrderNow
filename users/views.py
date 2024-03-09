"""
Users view module
"""

from rest_framework import viewsets, permissions

from users.permissions import IsPostRequest
from users.serializers import UserSerializer
from users.models import Users


class UserViewSet(viewsets.ModelViewSet):
    """
    Users view class for registration, retrieve and updation of users
    """

    serializer_class = UserSerializer
    permission_classes = [IsPostRequest | permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Get the list of items for this view
        """

        return Users.objects.filter(pk=self.request.user.id)
