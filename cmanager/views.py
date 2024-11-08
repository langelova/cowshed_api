"""
Views for the cow APIs.
"""

from rest_framework import viewsets
from .models import Cow
from .serializers import CowSerializer
from .filters import CowFilter
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend


class CowViewSet(viewsets.ModelViewSet):
    """View for managing cow APIs."""

    # ModelViewSet includes all CRUD operations: create, retrieve, update, delete
    queryset = Cow.objects.all()
    serializer_class = CowSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CowFilter
