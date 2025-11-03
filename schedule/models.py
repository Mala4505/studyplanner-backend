from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    icon = models.CharField(max_length=5, blank=True)
    category = models.CharField(max_length=30, blank=True)
    is_block_only = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    
class StudyBlock(models.Model):
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE)
    date_gregorian = models.DateField()
    date_hijri = models.CharField(max_length=20)
    day_of_week = models.CharField(max_length=10)
    page_start = models.PositiveIntegerField()
    page_end = models.PositiveIntegerField()
    tag = models.ForeignKey(Tag, null=True, blank=True, on_delete=models.SET_NULL)
    

