from django_filters import FilterSet
from .models import *


class CarFilter(FilterSet):
    class Meta:
        model = Car
        fields = {
            'brand': ['exact'],
            'model': ['exact'],
            'year': ['exact'],
            'price': ['gt', 'lt'],

        }
