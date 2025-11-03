from django.db import models
from users.models import User
from schedule.models import Tag

class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    page_from = models.PositiveIntegerField()
    page_to = models.PositiveIntegerField()
    duration_days = models.PositiveIntegerField()
    tag = models.ForeignKey(Tag, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_pages(self):
        return self.page_to - self.page_from + 1
