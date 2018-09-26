from django.http import HttpResponse
from api.models import Reading
from api.serializers import ReadingSerializer
import json

def index(request):
    readings = Reading.objects.all()
    serializer = ReadingSerializer(readings, many=True)
    return HttpResponse(json.dumps(serializer.data))