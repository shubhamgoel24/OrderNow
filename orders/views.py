"""
Orders view module
"""

from rest_framework import filters, generics, permissions, viewsets
from orders.models import Orders

from orders.permissions import IsRestaurantActive, IsRestaurantOwner
from orders.serializers import OrdersSerializer


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


class OrderViewSet(viewsets.ModelViewSet):
    """
    Order viewset class
    """

    serializer_class = OrdersSerializer
    permission_classes = [permissions.IsAuthenticated, IsRestaurantActive]
    http_method_names = ["post", "get"]

    def get_queryset(self):
        return Orders.objects.filter(customer=self.request.user, restaurant=self.kwargs.get("restaurant_id"))


class UserOrdersListView(generics.ListAPIView):
    """
    User's orders list class
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrdersSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "total_amount",
        "restaurant__name",
        "items__item__name",
    ]
    ordering_fields = [
        "total_amount",
        "restaurant__name",
        "items__item__name",
    ]

    def get_queryset(self):
        return Orders.objects.filter(customer=self.request.user)
