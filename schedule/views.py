from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import StudyBlock
from books.models import Book
from .utils import generate_study_blocks
from datetime import datetime

class ScheduleBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        book_id = request.data.get('book_id')
        start_date = request.data.get('start_date')
        book = Book.objects.get(id=book_id, user=request.user)
        StudyBlock.objects.filter(book=book).delete()

        blocks = generate_study_blocks(book, datetime.strptime(start_date, '%Y-%m-%d').date())
        StudyBlock.objects.bulk_create(blocks)
        return Response({'message': 'Schedule created'})
