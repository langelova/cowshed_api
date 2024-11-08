from celery import shared_task
from croniter import croniter
from datetime import datetime
from .models import Cow
import logging

logger = logging.getLogger(__name__)


@shared_task
def feed_and_milk_cows(cow_id):
    try:
        cow = Cow.objects.get(id=cow_id)
        logger.info(f"Feeding cow {cow.name} at {datetime.now()}")
    except Cow.DoesNotExist:
        logger.info(f"Cow with ID {cow_id} does not exist.")
