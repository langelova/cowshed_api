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
def update_cow_weight(cow_id, new_weight):
    try:
        # Retrieve the Cow instance
        cow = Cow.objects.get(id=cow_id)

        # Update weight and last_measured fields
        cow.weight.mass_kg = round(new_weight, 2)
        cow.weight.last_measured = timezone.now()
        cow.weight.save()

        logger.info(f"Updated weight for Cow ID {cow_id} to {round(new_weight, 2)} kg.")
    except Cow.DoesNotExist:
        logger.error(f"Cow with ID {cow_id} does not exist.")
