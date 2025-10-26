from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book, StudyBlock
from .serializers import BookSerializer, StudyBlockSerializer
from datetime import timedelta

class BookCreateView(APIView):
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            book = serializer.save()

            # ✅ Generate StudyBlocks
            total_pages = book.total_pages
            duration = book.duration_days
            pages_per_day = (total_pages + duration - 1) // duration  # round up

            for day in range(duration):
                start_page = day * pages_per_day + 1
                end_page = min((day + 1) * pages_per_day, total_pages)
                date_gregorian = book.start_date + timedelta(days=day)

                StudyBlock.objects.create(
                    book=book,
                    date_gregorian=date_gregorian,
                    date_hijri='1447-04-02',  # Optional: compute dynamically
                    day_of_week=date_gregorian.strftime('%A'),
                    page_start=start_page,
                    page_end=end_page
                )

            return Response({
                "message": "Book and schedule saved",
                "id": book.id
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ScheduleCreateView(APIView):
    def post(self, request):
        serializer = StudyBlockSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Schedule saved"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ScheduleListView(APIView):
    def get(self, request):
        blocks = StudyBlock.objects.all()
        serializer = StudyBlockSerializer(blocks, many=True)
        return Response(serializer.data)

class UpdateBlockView(APIView):
    def patch(self, request):
        block_id = request.data.get("id")
        new_date = request.data.get("date_gregorian")
        try:
            block = StudyBlock.objects.get(id=block_id)
            block.date_gregorian = new_date
            block.save()
            return Response({"message": "Block updated"})
        except StudyBlock.DoesNotExist:
            return Response({"error": "Block not found"}, status=status.HTTP_404_NOT_FOUND)

