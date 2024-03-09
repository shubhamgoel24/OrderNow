"""
Serializers module
"""

from rest_framework import serializers
from restaurants.serializers import RestaurantSerializer
from django.contrib.auth.password_validation import validate_password

from users.models import Users


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            "username",
            "city",
            "state",
            "zipcode",
            "first_name",
            "last_name",
            "balance",
            "id",
            "email",
        ]
        read_only_fields = ["id"]


class UserSerializer(UserUpdateSerializer):
    """
    Serializer class for users
    """

    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = Users
        fields = UserUpdateSerializer.Meta.fields + [
            "password",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data: dict) -> Users:
        """
        Function for creation of a new user

        Args:
            validated_data (dict): validated user data

        Returns:
            Users: Created user object
        """

        user = Users.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserDetailsSerializer(UserSerializer):
    """
    Serializer class for users to show their restaurants
    """

    restaurants = RestaurantSerializer(many=True, read_only=True)

    class Meta:
        model = Users
        fields = UserSerializer.Meta.fields + [
            "restaurants",
        ]
        read_only_fields = ["id"]
