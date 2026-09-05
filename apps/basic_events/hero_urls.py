from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.basic_events.views import BibleReferenceViewSet, HeroImageViewSet
router = DefaultRouter()
router.register(r"bible-verses", BibleReferenceViewSet, basename="bible-verses")
router.register(r"images", HeroImageViewSet, basename="images")

urlpatterns = [
    path("", include(router.urls)),
]
