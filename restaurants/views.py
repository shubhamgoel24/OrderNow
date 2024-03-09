"""
Restaurants view module
"""

from rest_framework import viewsets
from rest_framework import permissions

from restaurants.models import Restaurants
from restaurants.permissions import IsOwnerOrReadOnly
from restaurants.serializers import RestaurantSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    """
    Restaurant viewset class
    """

    queryset = Restaurants.objects.filter(is_active=True)
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
