"""
Users view module
"""

from rest_framework import viewsets, status
from rest_framework.response import Response

from users.permissions import IsLoggedInUser
from users.serializers import UserSerializer
from users.models import Users


class UserViewSet(viewsets.ModelViewSet):
    """
    Users view class for registration, retreive and updation of users
    """

    serializer_class = UserSerializer
    permission_classes = [IsLoggedInUser]

    def get_queryset(self):
        """
        Get the list of items for this view
        """

        return Users.objects.filter(pk=self.request.user.id)

    def destroy(self, request, *args, **kwargs):
        """
        Function to handle deactivation of a user
        """

        user = request.user
        if not "pk" in kwargs or kwargs["pk"] != user.id:
            return Response(data={"message": "Invalid id provided"}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
