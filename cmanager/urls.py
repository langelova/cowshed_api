"""URL mappings for the cow API."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CowViewSet

router = DefaultRouter()
router.register("cows", CowViewSet)

# Include the router URLs
urlpatterns = [path("", include(router.urls))]
