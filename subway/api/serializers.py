from rest_framework import serializers
from api.models import Reading
from .models import Reading

class ReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reading
        fields = ('timestamp', 'line', 'status')
