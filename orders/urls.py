"""
Routes Module
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from orders.views import OrderViewSet, UserOrdersListView

app_name = "orders"

router = DefaultRouter()
router.register(r"orders", OrderViewSet, basename="orders")

urlpatterns = [
    path("restaurants/<int:restaurant_id>/", include(router.urls)),
    path("my-orders/", UserOrdersListView.as_view(), name="user_orders"),
]
