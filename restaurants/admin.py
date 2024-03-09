"""
Admin module for restaurants
"""

from django.contrib import admin

from restaurants.models import Menus, OrderItems, Orders, Restaurants

admin.site.register(Restaurants)
admin.site.register(Menus)
admin.site.register(Orders)
admin.site.register(OrderItems)
