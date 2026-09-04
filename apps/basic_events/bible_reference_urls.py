from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.basic_events.views import BibleReferenceViewSet
router = DefaultRouter()
router.register(r"", BibleReferenceViewSet, basename="bible-references")

urlpatterns = [
    path("", include(router.urls)),
]
