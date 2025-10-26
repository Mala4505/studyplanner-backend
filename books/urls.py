from django.urls import path
from .views import BookListCreateView

urlpatterns = [
    path('', BookListCreateView.as_view(), name='book-list-create'),
]
