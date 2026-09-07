from django.urls import path

from apps.basic_events.views import WelcomeContentView

urlpatterns = [
    path("", WelcomeContentView.as_view(), name="welcome-content"),
]