"""
Serializers module
"""

from rest_framework import serializers

from restaurants.models import Menus, Restaurants


class RestaurantSerializer(serializers.ModelSerializer):
    """
    Serializer class for restaurants
    """

    class Meta:
        model = Restaurants
        fields = ["name", "id"]
        read_only_fields = ["id"]

    def create(self, validated_data: dict) -> Restaurants:
        """
        Function for creation of a new restaurant

        Args:
            validated_data (dict): validated user data

        Returns:
            Restaurants: Created restaurant object
        """

        request = self.context.get("request")
        restaurant = Restaurants.objects.create(**validated_data, owner=request.user)
        request.user.is_restaurant_owner = True
        request.user.save()
        return restaurant


class MenuSerializer(serializers.ModelSerializer):
    """
    Serializer class for menus
    """

    class Meta:
        model = Menus
        read_only_fields = ["id"]
        exclude = ["restaurant"]

    def create(self, validated_data: dict) -> Restaurants:
        """
        Function for creation of a new menu

        Args:
            validated_data (dict): validated menu data

        Returns:
            Restaurants: Created Menu object
        """

        restaurant_id = self.context.get("view").kwargs["restaurant_id"]
        menu = Menus.objects.create(**validated_data, restaurant_id=restaurant_id)
        return menu
