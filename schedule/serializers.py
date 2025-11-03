from rest_framework import serializers
from .models import StudyBlock, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'icon', 'category', 'is_block_only']
        
class ScheduledBlockSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    tag = TagSerializer()
    bookTag = serializers.SerializerMethodField()
    
    class Meta:
        model = StudyBlock
        fields = [
            'id',
            'book',
            'book_title',  # ✅ Add this
            'date_gregorian',
            'date_hijri',
            'day_of_week',
            'page_start',
            'page_end',
            'tag',
            'bookTag',
        ]
    def get_bookTag(self, obj):
        return TagSerializer(obj.book.tag).data if obj.book.tag else None
