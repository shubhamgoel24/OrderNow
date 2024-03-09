"""
Routes Module
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from orders.views import OrderViewSet

app_name = "orders"

router = DefaultRouter()
router.register(r"orders", OrderViewSet, basename="orders")

urlpatterns = [
    path("", include(router.urls)),
]
