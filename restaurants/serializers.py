"""
Serializers module
"""

from rest_framework import serializers

from restaurants.models import Restaurants

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
        restaurant.save()
        return restaurant
