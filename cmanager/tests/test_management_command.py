from django.core.management import call_command
from django.test import TestCase

from cmanager.models import Cow, Feeding, MilkProduction, Weight


class GenerateRandomDataCommandTests(TestCase):

    def test_generate_random_data_command(self):
        """Test that the generate_random_data command creates the specified number of cows"""
        num_cows = 5
        call_command("generate_random_data", num_cows=num_cows)

        # Check that the cows are created
        self.assertEqual(Cow.objects.count(), num_cows)

        # Check that each cow has associated Feeding, MilkProduction (if female), and Weight data
        for cow in Cow.objects.all():
            # Check Feeding exists for each cow
            self.assertTrue(Feeding.objects.filter(cow=cow).exists())

            # Check MilkProduction exists for females
            if cow.sex == "Female":
                self.assertTrue(MilkProduction.objects.filter(cow=cow).exists())

            # Check Weight exists for each cow
            self.assertTrue(Weight.objects.filter(cow=cow).exists())
