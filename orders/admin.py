"""
Admin module for orders
"""

from django.contrib import admin

from orders.models import OrderItems, Orders

admin.site.register(Orders)
admin.site.register(OrderItems)
