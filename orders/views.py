"""
Orders view module
"""

from rest_framework import filters, permissions, viewsets

from orders.models import Orders
from orders.permissions import IsOwnerOrCustomer
from orders.serializers import OrdersSerializer, OrdersUpdateSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    Order viewset class
    """

    permission_classes = [permissions.IsAuthenticated, IsOwnerOrCustomer]
    http_method_names = ["post", "get", "patch"]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "total_amount",
        "customer__username",
        "restaurant__name",
        "items__item__name",
    ]
    ordering_fields = [
        "total_amount",
        "customer__username",
        "restaurant__name",
        "items__item__name",
    ]

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        """

        if self.action == "partial_update":
            return OrdersUpdateSerializer
        return OrdersSerializer

    def get_queryset(self):
        if self.action == "partial_update":
            return Orders.objects.all()

        restaurant_id = self.request.GET.get("restaurant_id")
        if restaurant_id:
            return Orders.objects.filter(
                restaurant_id=restaurant_id, restaurant__owner=self.request.user, restaurant__is_active=True
            )
        else:
            return Orders.objects.filter(customer=self.request.user)
