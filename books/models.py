from django.db import models
from users.models import User

class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    page_from = models.PositiveIntegerField()
    page_to = models.PositiveIntegerField()
    duration_days = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_pages(self):
        return self.page_to - self.page_from + 1
