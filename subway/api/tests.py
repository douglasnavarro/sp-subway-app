from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Reading
from django.contrib.auth.models import User, Permission
from .serializers import ReadingSerializer
from django.urls import reverse
from .test_data import test_data
from datetime import datetime


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
        response = self.client.get('/api/?timestamp_after=2018-09-11&timestamp_before=2018-09-21')
        expected = Reading.objects.filter(timestamp__range=(datetime(2018,9,11), datetime(2018,9,21)))
        serialized = ReadingSerializer(expected, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized.data)

class PostReadingsTest(BaseViewTest):

    def setUp(self):

        user = User.objects.create(username='test_user')
        user.set_password('test_user123')
        permission = Permission.objects.get(name='Can add reading')
        user.user_permissions.add(permission)
        user.save()

    def test_post_forbidden(self):
        payload = {'timestamp':'2018-09-12T10:00', 'line':'jade', 'status':'normal'}
        response = self.client.post('/api/', payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_post_allowed(self):
        self.client.login(username='test_user', password='test_user123')
        payload = {'timestamp':'2018-09-25T13:00', 'line':'safira', 'status':'paralisada'}
        response = self.client.post('/api/', payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.logout()