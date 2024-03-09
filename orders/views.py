"""
Orders view module
"""

from rest_framework import filters, permissions, viewsets

from orders.models import Orders
from orders.serializers import OrdersSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    Order viewset class
    """

    serializer_class = OrdersSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["post", "get"]
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

    def get_queryset(self):
        restaurant_id = self.request.GET.get("restaurant_id")
        if restaurant_id:
            return Orders.objects.filter(
                restaurant_id=restaurant_id, restaurant__owner=self.request.user, restaurant__is_active=True
            )
        else:
            return Orders.objects.filter(customer=self.request.user)
