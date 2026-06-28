from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.events.views import EventViewSet

router = DefaultRouter()
router.register(r"", EventViewSet, basename="events")

urlpatterns = [
    path("", include(router.urls)),
]
