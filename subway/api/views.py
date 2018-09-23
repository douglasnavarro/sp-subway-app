from rest_framework.generics import ListCreateAPIView
from api.models import Reading
from .serializers import ReadingSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ReadingsFilter

class ReadingsListView(ListCreateAPIView):
    queryset = Reading.objects.all()
    serializer_class = ReadingSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = ReadingsFilter
