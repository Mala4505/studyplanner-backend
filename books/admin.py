from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'page_from', 'page_to', 'duration_days')
    search_fields = ('title',)
    list_filter = ('user',)
