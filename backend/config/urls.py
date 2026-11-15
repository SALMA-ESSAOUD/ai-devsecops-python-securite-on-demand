from django.urls import include, path

urlpatterns = [
    path("api/health/", include("apps.health.urls")),
]
