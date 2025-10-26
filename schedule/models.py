from django.db import models
from books.models import Book

class StudyBlock(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_gregorian = models.DateField()
    date_hijri = models.CharField(max_length=20)
    day_of_week = models.CharField(max_length=10)
    page_start = models.PositiveIntegerField()
    page_end = models.PositiveIntegerField()
