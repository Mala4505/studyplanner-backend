from django.urls import path
from .views import ScheduleBookView

urlpatterns = [
    path('book/', ScheduleBookView.as_view(), name='schedule-book'),
]
