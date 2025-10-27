from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    pageFrom = serializers.IntegerField(source='page_from')
    pageTo = serializers.IntegerField(source='page_to')
    duration = serializers.IntegerField(source='duration_days')
    totalPages = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'pageFrom', 'pageTo', 'duration', 'totalPages']

    def get_totalPages(self, obj):
        return max(0, obj.page_to - obj.page_from + 1)
