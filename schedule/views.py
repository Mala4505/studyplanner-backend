from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import StudyBlock
from books.models import Book
from .utils import generate_study_blocks
from datetime import datetime
from .serializers import ScheduledBlockSerializer

class ScheduleListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        blocks = StudyBlock.objects.filter(book__user=request.user)
        serializer = ScheduledBlockSerializer(blocks, many=True)
        return Response(serializer.data)

class ScheduleBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        book_id = request.data.get('book_id')
        start_date = request.data.get('start_date')  # format: 'YYYY-MM-DD'

        try:
            book = Book.objects.get(id=book_id, user=request.user)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=404)

        StudyBlock.objects.filter(book=book).delete()

        blocks = generate_study_blocks(book, datetime.strptime(start_date, '%Y-%m-%d').date())
        StudyBlock.objects.bulk_create(blocks)

        return Response({'message': 'Schedule created'})
