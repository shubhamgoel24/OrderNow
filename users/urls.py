"""
Routes Module
"""

from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from users.views import UserViewSet


app_name = "users"

urlpatterns = [
    path("login/", jwt_views.TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("users/", UserViewSet.as_view({"post": "create", "get": "list"}), name="users"),
    path(
        "users/<int:pk>/",
        UserViewSet.as_view({"patch": "partial_update", "delete": "destroy"}),
        name="users",
    ),
]
