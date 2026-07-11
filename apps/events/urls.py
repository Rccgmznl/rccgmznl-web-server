from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.events.views import EventViewSet, GalleryImageUploadView

router = DefaultRouter()
router.register(r"", EventViewSet, basename="events")

urlpatterns = [
    path("uploads/gallery-image/", GalleryImageUploadView.as_view(), name="gallery-image-upload"),
    path("", include(router.urls)),
]
