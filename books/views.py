from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer

class BookListCreateView(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

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
