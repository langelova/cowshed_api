from celery import shared_task
from django.utils import timezone
from datetime import datetime
from .models import Cow
import logging

logger = logging.getLogger(__name__)


@shared_task
def feed_cow(cow_id):
    try:
        cow = Cow.objects.get(id=cow_id)
        logger.info(f"Feeding cow {cow.name} at {datetime.now()}")
    except Cow.DoesNotExist:
        logger.error(f"Cow with ID {cow_id} does not exist.")


@shared_task
def milk_cow(cow_id):
    try:
        cow = Cow.objects.get(id=cow_id)
        logger.info(f"Milikng cow {cow.name} at {datetime.now()}")
    except Cow.DoesNotExist:
        logger.error(f"Cow with ID {cow_id} does not exist.")


@shared_task
def update_animal_weight(cow_id, new_weight):
    try:
        # Retrieve the Animal instance
        cow = Cow.objects.get(id=cow_id)

        # Update weight and last_measured fields
        cow.weight.mass_kg = new_weight
        cow.weight.last_measured = timezone.now()
        cow.weight.save()

        logger.info(f"Updated weight for Animal ID {cow_id} to {new_weight} kg.")
    except Cow.DoesNotExist:
        logger.error(f"Animal with ID {cow_id} does not exist.")
