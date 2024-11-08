"""
Views for the cow APIs.
"""

import random
from rest_framework import viewsets
from .models import Cow
from .serializers import CowSerializer
from .filters import CowFilter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from .tasks import update_cow_weight


class CowViewSet(viewsets.ModelViewSet):
    """View for managing cow APIs."""

    # ModelViewSet includes all CRUD operations: create, retrieve, update, delete
    queryset = Cow.objects.all()
    serializer_class = CowSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CowFilter

    @action(detail=True, methods=["post"])
    def weigh(self, request, pk=None):
        """
        Custom action to weigh a cow and update its weight asynchronously.
        Generates a random weight between 1000 and 2000 kg.
        """
        cow = self.get_object()  # Get the specific animal instance
        random_weight = random.uniform(1000, 2000)  # Generate random weight

        # Trigger the async task to update the weight
        update_cow_weight.delay(cow.id, random_weight)

        return Response(
            {"message": "Weighing task enqueued successfully.", "generated_weight": random_weight},
            status=status.HTTP_202_ACCEPTED,
        )
