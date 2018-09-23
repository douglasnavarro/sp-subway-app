from django_filters import FilterSet, DateFromToRangeFilter
from .models import Reading

class ReadingsFilter(FilterSet):
    
    timestamp = DateFromToRangeFilter()

    class Meta:
        model = Reading
        fields = ['line', 'timestamp']