from django.test import TestCase
from django.utils import timezone
from cmanager.models import Cow, Feeding, MilkProduction, Weight
import random
from datetime import timedelta


class cowModelTests(TestCase):

    def setUp(self):
        # Set up a sample cow for testing
        self.cow = Cow.objects.create(
            name="TestCow",
            sex="F",
            birthdate=timezone.now() - timedelta(days=random.randint(365, 1825)),
            condition="healthy",
            has_calves=True,
            calves_id=1500,
        )
        # Set up Feeding for the cow
        self.feeding = Feeding.objects.create(
            cow=self.cow, amount_kg=5.0, cron_schedule="0 */6 * * *"
        )
        # Set up MilkProduction for the cow
        self.milk_production = MilkProduction.objects.create(
            cow=self.cow, amount_l=5.0, cron_schedule="0 */8 * * *"
        )
        # Set up Weight for the cow
        self.weight = Weight.objects.create(
            cow=self.cow, mass_kg=1200.0, last_measured=timezone.now() - timedelta(days=10)
        )

    def test_cow_creation(self):
        """Test that the cow is created correctly"""
        self.assertEqual(self.cow.name, "TestCow")
        self.assertEqual(self.cow.sex, "F")
        self.assertTrue(self.cow.has_calves)
        self.assertEqual(self.cow.calves_id, 1500)

    def test_feeding_creation(self):
        """Test that feeding is correctly linked to the cow"""
        self.assertEqual(self.feeding.cow, self.cow)
        self.assertEqual(self.feeding.amount_kg, 5.0)
        self.assertEqual(self.feeding.cron_schedule, "0 */6 * * *")

    def test_milk_production_creation(self):
        """Test that milk production is correctly linked to the cow"""
        self.assertEqual(self.milk_production.cow, self.cow)
        self.assertEqual(self.milk_production.amount_l, 5.0)
        self.assertEqual(self.milk_production.cron_schedule, "0 */8 * * *")

    def test_weight_creation(self):
        """Test that weight is correctly linked to the cow"""
        self.assertEqual(self.weight.cow, self.cow)
        self.assertAlmostEqual(self.weight.mass_kg, 1200.0)
        self.assertTrue(
            timezone.now() - timedelta(days=11)
            < self.weight.last_measured
            < timezone.now() - timedelta(days=9)
        )
