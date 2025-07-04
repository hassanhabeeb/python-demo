# products/filters.py
import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    stock_min = django_filters.NumberFilter(field_name="stock", lookup_expr='gte')
    stock_max = django_filters.NumberFilter(field_name="stock", lookup_expr='lte')

    class Meta:
        model = Product
        fields = {
            'name': ['exact', 'icontains'],
            'is_active': ['exact'],
            'created_at': ['date', 'date__gte', 'date__lte'],
        }
