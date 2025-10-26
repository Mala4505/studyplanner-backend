from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    total_pages = models.IntegerField()
    duration_days = models.IntegerField()
    start_date = models.DateField()

    def __str__(self):
        return self.title

class StudyBlock(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_gregorian = models.DateField()
    date_hijri = models.CharField(max_length=20)
    day_of_week = models.CharField(max_length=10)
    page_start = models.IntegerField()
    page_end = models.IntegerField()
