"""
Routes Module
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from users.views import UserViewSet

app_name = "users"
router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path("login/", jwt_views.TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]
