"""
Restaurants view module
"""

from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from restaurants.models import Menus, Restaurants
from restaurants.permissions import IsOwner, IsRestaurantOwner, ReadOnlyPermission
from restaurants.serializers import (
    MenuSerializer,
    MenuUpdateSerializer,
    RestaurantSerializer,
)


class RestaurantViewSet(viewsets.ModelViewSet):
    """
    Restaurant viewset class
    """

    queryset = Restaurants.objects.filter(is_active=True)
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated, ReadOnlyPermission | IsOwner]


class MenuViewSet(viewsets.ModelViewSet):
    """
    Menu viewset class
    """

    permission_classes = [permissions.IsAuthenticated, ReadOnlyPermission | IsRestaurantOwner]

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        """

        if self.request.method == "PATCH":
            return MenuUpdateSerializer
        return MenuSerializer

    def get_queryset(self):
        restaurant_id = self.kwargs["restaurant_id"]
        return Menus.objects.filter(restaurant__pk=restaurant_id, restaurant__is_active=True)

    def destroy(self, request, *args, **kwargs):
        return Response(
            {"detail": "DELETE method is not allowed for this resource."}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
