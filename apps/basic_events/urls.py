from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.basic_events.views import BasicEventViewSet
router = DefaultRouter()
router.register(r"", BasicEventViewSet, basename="basic-events")

urlpatterns = [
    path("", include(router.urls)),
]
