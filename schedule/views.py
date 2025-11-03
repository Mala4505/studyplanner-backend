from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import StudyBlock, Tag
from books.models import Book
from .utils import generate_study_blocks
from .serializers import ScheduledBlockSerializer, TagSerializer

import requests
from django.http import JsonResponse

from datetime import datetime
import pytz
import calendar
from hijri_converter import convert


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


class UpdateBlockView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, block_id):
        try:
            block = StudyBlock.objects.get(id=block_id, book__user=request.user)
        except StudyBlock.DoesNotExist:
            return Response({'error': 'Block not found'}, status=404)

        new_date = request.data.get('date_gregorian')
        tag_id = request.data.get('tag_id')

        if new_date:
            nairobi = pytz.timezone("Africa/Nairobi")
            greg_date = datetime.strptime(new_date, '%Y-%m-%d')
            localized_date = nairobi.localize(greg_date).date()

            block.date_gregorian = localized_date
            block.date_hijri = convert.Gregorian(
                localized_date.year,
                localized_date.month,
                localized_date.day
            ).to_hijri().isoformat()
            block.day_of_week = calendar.day_name[localized_date.weekday()]

        if tag_id is not None:
            try:
                tag = Tag.objects.get(id=tag_id)
                if not tag.is_block_only:
                    return Response({'error': 'This tag is not allowed for blocks'}, status=400)
                block.tag = tag
            except Tag.DoesNotExist:
                return Response({'error': 'Tag not found'}, status=404)

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


class UpdateBlockTagView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, block_id):
        try:
            block = StudyBlock.objects.get(id=block_id, book__user=request.user)
        except StudyBlock.DoesNotExist:
            return Response({'error': 'Block not found'}, status=404)

        tag_id = request.data.get('tag_id')
        if not tag_id:
            return Response({'error': 'Missing tag_id'}, status=400)

        try:
            tag = Tag.objects.get(id=tag_id)
            if not tag.is_block_only:
                return Response({'error': 'Tag is not allowed for blocks'}, status=400)
            block.tag = tag
            block.save()
            return Response({'message': 'Tag updated'})
        except Tag.DoesNotExist:
            return Response({'error': 'Tag not found'}, status=404)


class ClearBookScheduleView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        StudyBlock.objects.filter(book__user=user).delete()
        return Response({'message': 'Schedule removed for this book'})


class DeleteBookScheduleView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id, user=request.user)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=404)

        StudyBlock.objects.filter(book=book).delete()
        return Response({'message': 'Schedule removed for this book'})


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]


def hijri_date(request):
    date = request.GET.get('date')
    if not date:
        return JsonResponse({'error': 'Missing date'}, status=400)

    response = requests.get(f'https://api.aladhan.com/v1/gToH?date={date}')
    return JsonResponse(response.json())