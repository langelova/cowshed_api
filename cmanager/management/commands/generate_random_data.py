# generate_random_data.py
import logging
import random
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from cmanager.models import Cow, Feeding, MilkProduction, Weight

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Generate random data for the Cow, Feeding, and MilkProduction models."

    def add_arguments(self, parser):
        parser.add_argument(
            "--num_cows", type=int, default=10, help="The number of cows to create."
        )

    def handle(self, *args, **options):
        num_cows = options["num_cows"]

        # Define random choices and data ranges
        sex_choices = ["M", "F"]
        condition_choices = ["healthy", "sick", "injured"]
        current_time = timezone.now()

        # Create random Cows
        for i in range(num_cows):
            name = f"Cow_{i+1}"
            sex = random.choice(sex_choices)
            condition = random.choice(condition_choices)

            # Add random hours and minutes
            birthdate = current_time - timedelta(days=random.randint(365, 1825))
            has_calves = random.choice([True, False])
            calves_id = random.randint(1000, 2000) if has_calves else None

            try:
                cow = Cow.objects.create(
                    name=name,
                    sex=sex,
                    birthdate=birthdate,
                    condition=condition,
                    has_calves=has_calves,
                    calves_id=calves_id,
                )
            except Exception as e:
                logger.error(f"Error with creating cow data: {e}")
                return

            # Create Feeding data for the cow
            feeding_amount_kg = round(random.uniform(3, 10), 2)
            feeding_cron_schedule = (
                "0 */6 * * *"  # Example cron for feeding every 6 hours
            )
            try:
                Feeding.objects.create(
                    cow=cow,
                    amount_kg=feeding_amount_kg,
                    cron_schedule=feeding_cron_schedule,
                )
            except Exception as e:
                logger.error(f"Error with creating feeding data: {e}")
                return

            # Create MilkProduction data for the cow
            if sex == "F":  # Assuming only females produce milk
                milk_amount_l = round(random.uniform(2, 10), 2)
                milk_cron_schedule = (
                    "0 */8 * * *"  # Example cron for milking every 8 hours
                )
                try:
                    MilkProduction.objects.create(
                        cow=cow,
                        amount_l=milk_amount_l,
                        cron_schedule=milk_cron_schedule,
                    )
                except Exception as e:
                    logger.error(f"Error with creating milk production data: {e}")
                    return

            # Create Weight data for the animal
            weight_kg = round(
                random.uniform(500, 1500), 2
            )  # Random weight between 500 and 1500 kg
            last_measured = current_time - timedelta(
                days=random.randint(1, 30)
            )  # Measured within the last month
            try:
                Weight.objects.create(
                    cow=cow, mass_kg=weight_kg, last_measured=last_measured
                )
            except Exception as e:
                logger.error(f"Error with creating weight production data: {e}")
                return

            self.stdout.write(
                self.style.SUCCESS(
                    f"Created Cow: {name} with Feeding and MilkProduction (if female)"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {num_cows} cows with random data."
            )
        )
