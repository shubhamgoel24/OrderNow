"""
Routes Module
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from restaurants.views import MenuViewSet, RestaurantViewSet

app_name = "restaurants"

router = DefaultRouter()
router.register(r"restaurants", RestaurantViewSet, basename="restaurants")

menu_router = DefaultRouter()
menu_router.register(r"menus", MenuViewSet, basename="menus")

urlpatterns = [
    path("", include(router.urls)),
    path("restaurants/<int:restaurant_id>/", include(menu_router.urls)),
]
