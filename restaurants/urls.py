"""
Routes Module
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from restaurants.views import MenuViewSet, RestaurantOrdersList, RestaurantViewSet

app_name = "restaurants"

router = DefaultRouter()
router.register(r"restaurants", RestaurantViewSet, basename="restaurants")
router.register(r"restaurants/(?P<restaurant_id>[^/.]+)/menus", MenuViewSet, basename="restaurant-menus")

urlpatterns = [
    path("", include(router.urls)),
    path("restaurants/<int:restaurant_id>/all-orders/", RestaurantOrdersList.as_view(), name="restaurant_orders"),
]
