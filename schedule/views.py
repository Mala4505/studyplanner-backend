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
    
# class UpdateBlockView(APIView):
#     permission_classes = [IsAuthenticated]

#     def patch(self, request, block_id):
#         try:
#             block = StudyBlock.objects.get(id=block_id, book__user=request.user)
#         except StudyBlock.DoesNotExist:
#             return Response({'error': 'Block not found'}, status=404)

#         new_date = request.data.get('date_gregorian')
#         if new_date:
#             block.date_gregorian = datetime.strptime(new_date, '%Y-%m-%d').date()
#             block.save()
#             return Response({'message': 'Block updated'})
#         return Response({'error': 'Missing date_gregorian'}, status=400)

class UpdateBlockView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, block_id):
        try:
            block = StudyBlock.objects.get(id=block_id, book__user=request.user)
        except StudyBlock.DoesNotExist:
            return Response({'error': 'Block not found'}, status=404)

        new_date = request.data.get('date_gregorian')
        if not new_date:
            return Response({'error': 'Missing date_gregorian'}, status=400)

        # Update the block's date
        block.date_gregorian = datetime.strptime(new_date, '%Y-%m-%d').date()
        block.save()

        # Reorder all blocks for this book
        all_blocks = StudyBlock.objects.filter(book=block.book).order_by('date_gregorian')
        start_page = block.book.page_from
        total_pages = block.book.total_pages
        num_blocks = all_blocks.count()
        pages_per_block = total_pages // num_blocks
        remainder = total_pages % num_blocks

        current_page = start_page
        for i, b in enumerate(all_blocks):
            extra = 1 if i < remainder else 0
            b.page_start = current_page
            b.page_end = current_page + pages_per_block + extra - 1
            current_page = b.page_end + 1

        StudyBlock.objects.bulk_update(all_blocks, ['page_start', 'page_end'])

        return Response({'message': 'Block updated and sequence adjusted'})

class RescheduleBlockView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        block_id = request.data.get('block_id')
        new_date = request.data.get('new_date')

        try:
            block = StudyBlock.objects.get(id=block_id, book__user=request.user)
        except StudyBlock.DoesNotExist:
            return Response({'error': 'Block not found'}, status=404)

        block.date_gregorian = datetime.strptime(new_date, '%Y-%m-%d').date()
        block.save()

        return Response({'message': 'Block rescheduled'})
