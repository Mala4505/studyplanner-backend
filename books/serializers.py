from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    total_pages = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'page_from', 'page_to', 'duration_days', 'total_pages']
