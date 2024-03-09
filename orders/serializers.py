"""
Serializers module
"""

from django.db import transaction
from rest_framework import serializers

from orders.models import OrderItems, Orders
from restaurants.models import Menus
from users.models import Users


class OrderItemsSerializer(serializers.ModelSerializer):
    """
    Serializer class for order items
    """

    item = serializers.SlugRelatedField(read_only=True, slug_field="name")
    price = serializers.ReadOnlyField()
    id = serializers.IntegerField()

    class Meta:
        model = OrderItems
        fields = ["price", "quantity", "id", "item"]


class OrdersSerializer(serializers.ModelSerializer):
    """
    Serializer class for orders
    """

    restaurant = serializers.SlugRelatedField(read_only=True, slug_field="name")
    customer = serializers.SlugRelatedField(read_only=True, slug_field="username")
    items = OrderItemsSerializer(many=True)

    def validate_items(self, items):
        """
        Validate that the items list is not empty.
        """

        if not items:
            raise serializers.ValidationError("At least one item is required.")
        return items

    class Meta:
        model = Orders
        fields = "__all__"
        read_only_fields = ["id", "order_datetime", "total_amount", "status", "address", "contact"]

    def create(self, validated_data: dict) -> Orders:
        """
        Function for creation of a new order

        Args:
            validated_data (dict): validated order data

        Returns:
            Orders: Created order object
        """

        request = self.context.get("request")
        items_data = validated_data.pop("items", [])

        try:
            with transaction.atomic():
                customer = Users.objects.select_for_update().get(pk=request.user.id)
                if not customer.phone_number:
                    raise serializers.ValidationError(
                        {"Profile": "Phone number is required for placing order. Please update it."}
                    )
                required_address_fields = ["street_address", "state", "city", "zipcode"]
                missing_fields = [field for field in required_address_fields if not getattr(customer, field)]
                if missing_fields:
                    raise serializers.ValidationError(
                        {
                            "Profile": f"Please update complete address first. Missing fields: {', '.join(missing_fields)}."
                        }
                    )

                total_amount = 0
                restaurant = None
                order = None

                for item_data in items_data:
                    item_id = item_data.get("id")
                    quantity = item_data.get("quantity")

                    menu_item = Menus.objects.select_for_update().get(pk=item_id)

                    if not restaurant:
                        restaurant = menu_item.restaurant
                        if not restaurant.is_active:
                            raise serializers.ValidationError({"Items": f"Invalid item id: {item_id}"})
                        order = Orders.objects.create(
                            **validated_data, total_amount=0, customer=customer, restaurant=restaurant
                        )
                    elif restaurant != menu_item.restaurant:
                        raise serializers.ValidationError({"Items": "Select all items from same restaurant"})

                    if menu_item.quantity < quantity:
                        raise serializers.ValidationError(
                            {"Items": f"Not enough quantity available for item: {menu_item.name}"}
                        )

                    order_item = OrderItems.objects.create(
                        order=order,
                        item=menu_item,
                        price=menu_item.price,
                        quantity=quantity,
                    )

                    total_amount += order_item.price * quantity

                    menu_item.quantity -= quantity
                    menu_item.save()

                order.total_amount = total_amount
                order.contact = customer.phone_number
                order.address = f"{customer.street_address}, {customer.city}, {customer.state}, {customer.zipcode}"
                order.save()

                if customer.balance < total_amount:
                    raise serializers.ValidationError({"Profile": f"Not enough balance"})
                customer.balance -= total_amount
                customer.save()
        except Menus.DoesNotExist:
            raise serializers.ValidationError({"Items": f"Invalid item id: {item_id}"})

        return order
