from django.urls import path
from .views import *

urlpatterns = [
    path('', ScheduleListView.as_view(), name='schedule-list'),
    path('book/', ScheduleBookView.as_view(), name='schedule-book'),
    path('block/<int:block_id>/', UpdateBlockView.as_view(), name='update-block'),
    path('reschedule/', RescheduleBlockView.as_view(), name='reschedule-block'),
]
