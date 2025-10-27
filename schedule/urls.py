from django.urls import path
from .views import ScheduleListView, ScheduleBookView

urlpatterns = [
    path('', ScheduleListView.as_view(), name='schedule-list'),
    path('book/', ScheduleBookView.as_view(), name='schedule-book'),  # ✅ This exposes POST /schedule/book/
]
