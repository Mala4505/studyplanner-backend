from django.urls import path
from .views import *

urlpatterns = [
    path('', ScheduleListView.as_view(), name='schedule-list'),
    path('hijri/', hijri_date, name='hijri-date'),
    path('book/', ScheduleBookView.as_view(), name='schedule-book'),
    path('block/<int:block_id>/', UpdateBlockView.as_view(), name='update-block'),
    # path('reschedule/', RescheduleBlockView.as_view(), name='reschedule-block'),
    path('clear/', ClearBookScheduleView.as_view(), name='clear-schedule'),
    path('book/<int:book_id>/delete/', DeleteBookScheduleView.as_view(), name='delete-schedule'),
    path('<int:block_id>/tag/', UpdateBlockTagView.as_view(), name='update-block-tag'),


]
