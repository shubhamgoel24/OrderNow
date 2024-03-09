"""
Restaurants view module
"""

from rest_framework import filters, generics, permissions, status, viewsets
from rest_framework.response import Response

from orders.models import Orders
from orders.serializers import OrdersSerializer
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


class RestaurantOrdersList(generics.ListAPIView):
    """
    Restaurant's orders list view
    """

    permission_classes = [permissions.IsAuthenticated, IsRestaurantOwner]
    serializer_class = OrdersSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "total_amount",
        "customer__username",
    ]
    ordering_fields = ["total_amount", "customer__username"]

    def get_queryset(self):
        restaurant_id = self.kwargs.get("restaurant_id")
        return Orders.objects.filter(restaurant_id=restaurant_id)
