"""
Serializers for the cow APIs.
"""

from rest_framework import serializers

from .models import Cow, Feeding, MilkProduction, Weight


class WeightSerializer(serializers.ModelSerializer):
    """Serializer for the weight model."""

    class Meta:
        model = Weight
        fields = ["mass_kg", "last_measured"]


class FeedingSerializer(serializers.ModelSerializer):
    """Serializer for the feed model."""

    class Meta:
        model = Feeding
        fields = ["amount_kg", "cron_schedule"]


class MilkProductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MilkProduction
        fields = ["amount_l", "cron_schedule"]


class CowSerializer(serializers.ModelSerializer):
    """Serializer for the cow mdoel."""

    weight = WeightSerializer(required=False)
    feeding = FeedingSerializer(required=False)
    milk_production = MilkProductionSerializer(required=False)

    class Meta:
        model = Cow
        fields = [
            "id",
            "name",
            "sex",
            "birthdate",
            "condition",
            "weight",
            "feeding",
            "milk_production",
            "has_calves",
            "calves_id",
        ]

    def create(self, validated_data):
        weight_data = validated_data.pop("weight", None)
        feeding_data = validated_data.pop("feeding", None)
        milk_production_data = validated_data.pop("milk_production", None)

        cow = Cow.objects.create(**validated_data)

        if weight_data:
            Weight.objects.create(cow=cow, **weight_data)
        if feeding_data:
            Feeding.objects.create(cow=cow, **feeding_data)
        if milk_production_data:
            MilkProduction.objects.create(cow=cow, **milk_production_data)

        return cow

    def update(self, instance, validated_data):
        weight_data = validated_data.pop("weight", None)
        feeding_data = validated_data.pop("feeding", None)
        milk_production_data = validated_data.pop("milk_production", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if weight_data:
            Weight.objects.update_or_create(cow=instance, defaults=weight_data)
        if feeding_data:
            Feeding.objects.update_or_create(cow=instance, defaults=feeding_data)
        if milk_production_data:
            MilkProduction.objects.update_or_create(
                cow=instance, defaults=milk_production_data
            )

        return instance
