"""
Serializers module
"""

from rest_framework import serializers

from users.models import Users


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class for users
    """

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Users
        fields = [
            "username",
            "city",
            "state",
            "zipcode",
            "password",
            "first_name",
            "last_name",
            "balance",
            "id",
            "email",
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

    def update(self, instance: Users, validated_data: dict) -> Users:
        """
        Function to update a user

        Args:
            instance (Users): Instance of user to be updated
            validated_data (dict): Data to update user

        Returns:
            Users: Updated user instance
        """

        instance.email = validated_data.get("email", instance.email)
        instance.city = validated_data.get("city", instance.city)
        instance.state = validated_data.get("state", instance.state)
        instance.zipcode = validated_data.get("zipcode", instance.zipcode)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.balance = validated_data.get("balance", instance.balance)

        instance.save()
        return instance
