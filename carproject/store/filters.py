from django_filters import FilterSet
from .models import Car

class CarFilter(FilterSet):
    class Meta:
        model = Car
        fields = {
            'car_make' : ['exact'],
            'car_model': ['exact'],
            'year' : ['gt', 'lt'],
            'price': ['gt', 'lt'],
        }