"""
Routes Module
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from restaurants.views import (
    MenuViewSet,
    OrderViewSet,
    RestaurantOrdersList,
    RestaurantViewSet,
    UserOrdersListView,
)

app_name = "restaurants"

router = DefaultRouter()
router.register(r"restaurants", RestaurantViewSet, basename="restaurants")
router.register(r"restaurants/(?P<restaurant_id>[^/.]+)/menus", MenuViewSet, basename="menus")
router.register(r"restaurants/(?P<restaurant_id>[^/.]+)/orders", OrderViewSet, basename="orders")

urlpatterns = [
    path("", include(router.urls)),
    path("restaurants/<int:restaurant_id>/all-orders/", RestaurantOrdersList.as_view(), name="restaurant_orders"),
    path("my-orders/", UserOrdersListView.as_view(), name="user_orders"),
]
