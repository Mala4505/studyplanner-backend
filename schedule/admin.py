from django.contrib import admin
from .models import StudyBlock

@admin.register(StudyBlock)
class StudyBlockAdmin(admin.ModelAdmin):
    list_display = ('book', 'date_gregorian', 'date_hijri', 'page_start', 'page_end')
    list_filter = ('date_gregorian', 'book')
