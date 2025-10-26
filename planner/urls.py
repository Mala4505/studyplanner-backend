from django.urls import path
from .views import BookCreateView, ScheduleCreateView, ScheduleListView, UpdateBlockView

urlpatterns = [
    path('books/', BookCreateView.as_view()),
    path('schedule/', ScheduleListView.as_view()),       # GET
    path('schedule/save/', ScheduleCreateView.as_view()), # POST
    path('schedule/update/', UpdateBlockView.as_view()),  # PATCH
]
