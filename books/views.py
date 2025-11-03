from rest_framework import generics, status,viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Book
from schedule.models import StudyBlock
from .serializers import BookSerializer
from schedule.serializers import ScheduledBlockSerializer

class BookListCreateView(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only books created by the authenticated user
        return Book.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Save the book with the current user as owner
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Override to return cleaner response with totalPages included
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Book.objects.filter(user=self.request.user)


class StudyBlockViewSet(viewsets.ModelViewSet):
    queryset = StudyBlock.objects.all()
    serializer_class = ScheduledBlockSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StudyBlock.objects.filter(book__user=self.request.user)
