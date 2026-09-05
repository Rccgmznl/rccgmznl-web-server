from django.urls import path
from apps.basic_events.views import AboutViewSet

urlpatterns = [
    path("", AboutViewSet.as_view({"get": "list", "post": "create"}), name="about-list"),
    path("<int:pk>/", AboutViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}), name="about-detail"),
]