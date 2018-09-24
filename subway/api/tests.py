from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Reading
from .serializers import ReadingSerializer
from django.urls import reverse
from .test_data import test_data

class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_reading(timestamp, status, line):
        if 'timestamp' != "" and 'line' != "" and status != "":
            Reading.objects.create(timestamp=timestamp, line=line, status=status)
    
    def setUp(self):
        for reading in test_data:
            self.create_reading(**reading)
    
class GetAllReadingsTest(BaseViewTest):

    def test_get_all_readings(self):
        response = self.client.get('/api/')
        expected = Reading.objects.all()
        serialized = ReadingSerializer(expected, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized.data)
        
    def test_line_filter(self):
        response = self.client.get('/api/?line=vermelha')
        expected = Reading.objects.filter(line='vermelha')
        serialized = ReadingSerializer(expected, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized.data)
    
    def test_timestamp_filter(self):
        response = self.client.get('/api/')