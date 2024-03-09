"""
Restaurants view module
"""

from rest_framework import viewsets, status
from rest_framework.response import Response
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

    def destroy(self, request, *args, **kwargs):
        """
        Function to handle deactivation of a restaurant
        """

        restaurant = self.get_object()
        restaurant.is_active = False
        restaurant.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
