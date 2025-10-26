from rest_framework import serializers
from .models import Book, StudyBlock

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class StudyBlockSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = StudyBlock
        fields = [
            'id', 'book', 'book_title',
            'date_gregorian', 'date_hijri',
            'day_of_week', 'page_start', 'page_end'
        ]
