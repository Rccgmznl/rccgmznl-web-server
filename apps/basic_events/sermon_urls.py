from django.urls import path
from apps.basic_events.views import SermonViewSet

urlpatterns = [
    path("", SermonViewSet.as_view({"get": "list", "post": "create"}), name="sermon-list"),
    path("<int:pk>/", SermonViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}), name="sermon-detail"),
]