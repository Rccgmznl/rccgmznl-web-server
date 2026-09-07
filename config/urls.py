"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    
    # API Documentation
    path(
        f"api/{settings.API_DEFAULT_VERSION}/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        f"api/{settings.API_DEFAULT_VERSION}/schema/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        f"api/{settings.API_DEFAULT_VERSION}    /schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    
    # API v1
    path(
        f"api/{settings.API_DEFAULT_VERSION}/auth/",
        include("apps.users.urls"),
    ),
    # path(f"api/{settings.API_DEFAULT_VERSION}/events/", include("apps.events.urls")),
    path(f"api/{settings.API_DEFAULT_VERSION}/events/", include("apps.basic_events.urls")),
    path(f"api/{settings.API_DEFAULT_VERSION}/hero/", include("apps.basic_events.hero_urls")),
    path(f"api/{settings.API_DEFAULT_VERSION}/about/", include("apps.basic_events.about_urls")),
    path(f"api/{settings.API_DEFAULT_VERSION}/home-page/welcome/", include("apps.basic_events.welcome_urls")),
    path(f"api/{settings.API_DEFAULT_VERSION}/sermons/", include("apps.basic_events.sermon_urls")),
   
    
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )