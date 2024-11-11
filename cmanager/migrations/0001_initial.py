# Generated by Django 5.1.2 on 2024-11-07 17:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Cow",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                (
                    "sex",
                    models.CharField(
                        choices=[("M", "Male"), ("F", "Female")], max_length=1
                    ),
                ),
                ("birthdate", models.DateTimeField()),
                (
                    "condition",
                    models.CharField(
                        choices=[
                            ("healthy", "Healthy"),
                            ("sick", "Sick"),
                            ("injured", "Injured"),
                        ],
                        max_length=50,
                    ),
                ),
                ("has_calves", models.BooleanField()),
                ("calves_id", models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Feeding",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount_kg", models.FloatField()),
                ("cron_schedule", models.CharField(max_length=100)),
                (
                    "cow",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="feeding",
                        to="cmanager.cow",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MilkProduction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount_l", models.FloatField()),
                ("cron_schedule", models.CharField(max_length=100)),
                (
                    "cow",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="milk_production",
                        to="cmanager.cow",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Weight",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("mass_kg", models.FloatField()),
                ("last_measured", models.DateTimeField()),
                (
                    "cow",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="weight",
                        to="cmanager.cow",
                    ),
                ),
            ],
        ),
    ]
