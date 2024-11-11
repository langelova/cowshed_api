from django_filters import rest_framework as filters

from .models import Cow


class CowFilter(filters.FilterSet):
    """Sex, condition and weight filters for the cow objects."""

    sex = filters.CharFilter(field_name="sex", lookup_expr="iexact")
    condition = filters.CharFilter(field_name="condition", lookup_expr="icontains")
    min_weight = filters.NumberFilter(field_name="weight__mass_kg", lookup_expr="gte")
    max_weight = filters.NumberFilter(field_name="weight__mass_kg", lookup_expr="lte")

    class Meta:
        model = Cow
        fields = ["sex", "condition", "min_weight", "max_weight"]
