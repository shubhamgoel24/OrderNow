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
            validated_data (dict): validated restaurant data

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

    def create(self, validated_data: dict) -> Menus:
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


class MenuUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer class for menu update
    """

    class Meta:
        model = Menus
        read_only_fields = ["id", "name"]
        exclude = ["restaurant"]


class DateRangeInputSerializer(serializers.Serializer):
    """
    Date range input serializer
    """

    from_date = serializers.DateField(required=False, allow_null=True)
    to_date = serializers.DateField(required=False, allow_null=True)

    def validate(self, data):
        from_date = data.get("from_date")
        to_date = data.get("to_date")

        if (from_date or to_date) and not (to_date and from_date):
            raise serializers.ValidationError({"Params": "Please provide both 'from_date' and 'to_date'"})

        return data
