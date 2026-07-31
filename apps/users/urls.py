from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.users.views import (
    AuthViewSet,
    CustomTokenObtainPairView,
    TokenRefreshView,
)

# Create a router for the auth viewset
router = DefaultRouter()
router.register(r"", AuthViewSet, basename="auth")

urlpatterns = [
    # Auth viewset routes (register, me, change-password, logout)
    path("", include(router.urls)),
    
    # JWT token endpoints
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
