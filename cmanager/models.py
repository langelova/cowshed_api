"""
Database models.
"""

from django.db import models
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json
import logging

logger = logging.getLogger(__name__)


class Cow(models.Model):
    """Cow object representation."""

    SEX_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    CONDITION_CHOICES = [
        ("healthy", "Healthy"),
        ("sick", "Sick"),
        ("injured", "Injured"),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    birthdate = models.DateTimeField()
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES)
    has_calves = models.BooleanField()
    calves_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Weight(models.Model):
    """Weight object representation."""

    cow = models.OneToOneField(Cow, on_delete=models.CASCADE, related_name="weight")
    mass_kg = models.FloatField()
    last_measured = models.DateTimeField()

    def __str__(self):
        return f"{self.mass_kg} kg (measured on {self.last_measured})"


class Feeding(models.Model):
    cow = models.OneToOneField(Cow, on_delete=models.CASCADE, related_name="feeding")
    amount_kg = models.FloatField()
    cron_schedule = models.CharField(max_length=100)  # e.g., '0 */6 * * *'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.cron_schedule:
            self.update_celery_beat_schedule()

    def update_celery_beat_schedule(self):
        cron_parts = self.cron_schedule.split()
        if len(cron_parts) != 5:
            raise ValueError("Invalid cron schedule format")

        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=cron_parts[0],
            hour=cron_parts[1],
            day_of_month=cron_parts[2],
            month_of_year=cron_parts[3],
            day_of_week=cron_parts[4],
        )

        task_name = f"feed-cow-{self.cow.id}"
        PeriodicTask.objects.update_or_create(
            name=task_name,
            defaults={
                "task": "cmanager.tasks.feed_and_milk_cows",
                "crontab": schedule,
                "args": json.dumps([self.cow.id]),
            },
        )

    def delete(self, *args, **kwargs):
        task_name = f"feed-cow-{self.cow.id}"
        try:
            task = PeriodicTask.objects.get(name=task_name)
            task.delete()
        except PeriodicTask.DoesNotExist:
            pass
        super().delete(*args, **kwargs)


class MilkProduction(models.Model):
    cow = models.OneToOneField(Cow, on_delete=models.CASCADE, related_name="milk_production")
    amount_l = models.FloatField()
    cron_schedule = models.CharField(max_length=100)  # e.g., '0 */6 * * *'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.cron_schedule:
            self.update_celery_beat_schedule()

    def update_celery_beat_schedule(self):
        cron_parts = self.cron_schedule.split()
        if len(cron_parts) != 5:
            raise ValueError("Invalid cron schedule format")

        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=cron_parts[0],
            hour=cron_parts[1],
            day_of_month=cron_parts[2],
            month_of_year=cron_parts[3],
            day_of_week=cron_parts[4],
        )

        task_name = f"milk-cow-{self.cow.id}"
        PeriodicTask.objects.update_or_create(
            name=task_name,
            defaults={
                "task": "cmanager.tasks.feed_and_milk_cows",
                "crontab": schedule,
                "args": json.dumps([self.cow.id]),
            },
        )

    def delete(self, *args, **kwargs):
        task_name = f"milk-cow-{self.cow.id}"
        try:
            task = PeriodicTask.objects.get(name=task_name)
            task.delete()
        except PeriodicTask.DoesNotExist:
            pass
        super().delete(*args, **kwargs)
