"""
Routes Module
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from restaurants.views import RestaurantViewSet

app_name = "restaurants"

router = DefaultRouter()
router.register(r"restaurants", RestaurantViewSet, basename="restaurants")

urlpatterns = [
    path("", include(router.urls)),
]
