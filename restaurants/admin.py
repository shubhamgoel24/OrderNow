"""
Admin module for restaurants
"""

from django.contrib import admin

from restaurants.models import Menus, Restaurants

admin.site.register(Restaurants)
admin.site.register(Menus)
