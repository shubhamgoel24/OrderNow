"""
Users view module
"""

from django.db.models import Prefetch
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from restaurants.models import Restaurants

from users.permissions import IsPostRequest
from users.serializers import UserDetailsSerializer, UserSerializer, UserUpdateSerializer
from users.models import Users


class UserViewSet(viewsets.ModelViewSet):
    """
    Users view class for registration, retrieve and updation of users
    """

    permission_classes = [IsPostRequest | permissions.IsAuthenticated]

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        """

        if self.action == "retrieve" and self.request.user.is_restaurant_owner:
            return UserDetailsSerializer
        elif self.action == "partial_update":
            return UserUpdateSerializer
        return UserSerializer

    def get_queryset(self):
        """
        Get the list of items for this view
        """

        if self.action == "retrieve" and self.request.user.is_restaurant_owner:
            return Users.objects.prefetch_related(
                Prefetch("restaurants", queryset=Restaurants.objects.filter(is_active=True))
            ).filter(pk=self.request.user.id)

        return Users.objects.filter(pk=self.request.user.id)

    @action(detail=False, methods=["patch"], url_path="update_without_id")
    def custom_patch_method(self, request):
        """
        Custom method to update user details without id
        """

        self.kwargs["pk"] = self.request.user.id
        return self.partial_update(request=request)
