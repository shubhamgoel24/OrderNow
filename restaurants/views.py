"""
Restaurants view module
"""

from django.db import connection, models
from django.db.models.functions import RowNumber
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from orders.models import Orders
from restaurants.models import Menus, Restaurants
from restaurants.permissions import IsOwner, IsRestaurantOwner, ReadOnlyPermission
from restaurants.serializers import (
    DateRangeInputSerializer,
    MenuSerializer,
    MenuUpdateSerializer,
    RestaurantSerializer,
)
from users.models import Users


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


class ReportsViewset(viewsets.ViewSet):
    """
    Restaurant reports view
    """

    permission_classes = [permissions.IsAuthenticated, IsRestaurantOwner]

    @action(detail=False, methods=["get"], url_path="customer-spends")
    def customer_spends_report(self, request, restaurant_id):
        serializer = DateRangeInputSerializer(
            data={"from_date": request.query_params.get("from_date"), "to_date": request.query_params.get("to_date")}
        )
        serializer.is_valid(raise_exception=True)
        from_date = serializer.validated_data.get("from_date")
        to_date = serializer.validated_data.get("to_date")

        orders_query = Orders.objects.filter(restaurant_id=restaurant_id)
        if from_date and to_date:
            orders_query = orders_query.filter(order_datetime__range=[from_date, to_date])

        customer_spends = orders_query.values(user_email=models.F("customer__email")).annotate(
            total_amount_spent=models.Sum("total_amount")
        )

        return Response(customer_spends)

    @action(detail=False, methods=["get"], url_path="item-popularity")
    def item_popularity_report(self, request, restaurant_id):
        orders_query = Orders.objects.filter(restaurant_id=restaurant_id)

        item_popularity = (
            orders_query.values(item=models.F("items__item__name"))
            .annotate(orders=models.Count("customer", distinct=True))
            .order_by("orders")
        )

        return Response(item_popularity)

    @action(detail=False, methods=["get"], url_path="customer-favorites")
    def customer_favorites_report(self, request, restaurant_id):
        orders_query = Users.objects.filter(orders__restaurant_id=restaurant_id)
        customer_orders = (
            orders_query.annotate(item_count=models.Count("orders__items__item"))
            .annotate(row=models.Window(RowNumber(), partition_by="email", order_by=models.F("item_count").desc()))
            .values("email", "orders__items__item__name", "item_count", "row")
        )

        raw_sql = f"SELECT * from ({customer_orders.query}) AS subquery WHERE `row` = 1;"
        with connection.cursor() as cursor:
            cursor.execute(raw_sql)
            rows = cursor.fetchall()

        result = []
        for row in rows:
            result.append({"email": row[0], "item_name": row[1], "item_count": row[2]})

        return Response(result)
