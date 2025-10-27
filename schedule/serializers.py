from rest_framework import serializers
from .models import StudyBlock

class ScheduledBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyBlock
        fields = ['id', 'book', 'date_gregorian', 'date_hijri', 'day_of_week', 'page_start', 'page_end']
