from django.urls import path
from apps.basic_events.views import AboutView

urlpatterns = [
    path("", AboutView.as_view(), name="about"),
]