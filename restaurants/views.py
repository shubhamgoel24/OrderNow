"""
Restaurants view module
"""

from rest_framework import viewsets
from rest_framework import permissions

from restaurants.models import Menus, Restaurants
from restaurants.permissions import IsOwnerOrReadOnly, IsRestaurantOwner
from restaurants.serializers import MenuSerializer, RestaurantSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    """
    Restaurant viewset class
    """

    queryset = Restaurants.objects.filter(is_active=True)
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class MenuViewSet(viewsets.ModelViewSet):
    """
    Menu viewset class
    """

    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated, IsRestaurantOwner]

    def get_queryset(self):
        restaurant_id = self.kwargs["restaurant_id"]
        return Menus.objects.filter(restaurant__pk=restaurant_id, restaurant__is_active=True)
