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


class OrdersUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer class for orders update
    """

    restaurant = serializers.SlugRelatedField(read_only=True, slug_field="name")
    customer = serializers.SlugRelatedField(read_only=True, slug_field="username")
    items = OrderItemsSerializer(read_only=True, many=True)

    class Meta:
        model = Orders
        fields = "__all__"
        read_only_fields = ["id", "order_datetime", "total_amount", "address", "contact"]

    def validate_status(self, status: str) -> str:
        """
        Validate status based on permission of user.

        Args:
            status (str): Status to be updated

        Returns:
            str: Validated status
        """

        request = self.context.get("request")
        instance = self.instance

        if request.user != instance.restaurant.owner:
            if instance.status != Orders.OrderStatuses.IN_PROGRESS:
                raise serializers.ValidationError(f"Order cannot be updated. Current status is: {instance.status}")
            elif status != Orders.OrderStatuses.CANCELLED:
                raise serializers.ValidationError("User can only cancel order.")

        return status

    def update(self, instance: Orders, validated_data: dict) -> Orders:
        """
        Function to update order status

        Args:
            instance (Orders): Instance of order being updated
            validated_data (dict): Validated data

        Returns:
            Orders: Updated instance of order
        """

        status = validated_data["status"]

        with transaction.atomic():
            order_instance = Orders.objects.select_for_update().get(pk=instance.id)
            if order_instance.status in [Orders.OrderStatuses.CANCELLED, Orders.OrderStatuses.DELIVERED]:
                raise serializers.ValidationError(
                    {"status": [f"Order cannot be updated. Current status is: {order_instance.status}"]}
                )

            if status == Orders.OrderStatuses.CANCELLED:
                customer = Users.objects.select_for_update().get(pk=instance.customer.id)
                customer.balance += order_instance.total_amount
                customer.save()
                order_instance.status = status
                order_instance.save()
            else:
                order_instance.status = status
                order_instance.save()

        return order_instance
