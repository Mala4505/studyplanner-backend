from rest_framework import serializers
from .models import Book
from schedule.models import Tag
from schedule.serializers import TagSerializer

class BookSerializer(serializers.ModelSerializer):
    pageFrom = serializers.IntegerField(source='page_from')
    pageTo = serializers.IntegerField(source='page_to')
    duration = serializers.IntegerField(source='duration_days')
    totalPages = serializers.SerializerMethodField()
    tag = TagSerializer(read_only=True)
    tag_id = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.filter(is_block_only=False),
        source='tag',
        write_only=True,
        required=False
    )

    class Meta:
        model = Book
        fields = ['id', 'title', 'pageFrom', 'pageTo', 'duration', 'totalPages', 'tag', 'tag_id']
        extra_kwargs = {
            'title': {'required': False},  # ✅ allow partial updates
        }
        
    def get_totalPages(self, obj):
        return max(0, obj.page_to - obj.page_from + 1)
