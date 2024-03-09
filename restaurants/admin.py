"""
Admin module for restaurants
"""

from django.contrib import admin

from restaurants.models import Restaurants

admin.site.register(Restaurants)
