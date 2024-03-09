"""
Routes Module
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from restaurants.views import MenuViewSet, ReportsViewset, RestaurantViewSet

app_name = "restaurants"

router = DefaultRouter()
router.register(r"restaurants", RestaurantViewSet, basename="restaurants")
router.register(r"restaurants/(?P<restaurant_id>[^/.]+)/menus", MenuViewSet, basename="menus")
router.register(r"restaurants/(?P<restaurant_id>[^/.]+)/reports", ReportsViewset, basename="reports")

urlpatterns = [
    path("", include(router.urls)),
]
