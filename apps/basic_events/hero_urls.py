from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.basic_events.views import BibleReferenceView, HeroImageViewSet
router = DefaultRouter()
router.register(r"images", HeroImageViewSet, basename="images")

urlpatterns = [
    path("bible-verse/", BibleReferenceView.as_view(), name="bible-verse"),
    path("", include(router.urls)),
]
