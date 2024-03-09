"""
Routes Module
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from restaurants.views import MenuViewSet, RestaurantViewSet

app_name = "restaurants"

router = DefaultRouter()
router.register(r"restaurants", RestaurantViewSet, basename="restaurants")
router.register(r"restaurants/(?P<restaurant_id>[^/.]+)/menus", MenuViewSet, basename="menus")

urlpatterns = [
    path("", include(router.urls)),
]
