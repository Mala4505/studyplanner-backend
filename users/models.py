from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    tr_number = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=10, choices=[('admin', 'Admin'), ('student', 'Student')])

    USERNAME_FIELD = 'tr_number'
    REQUIRED_FIELDS = ['username']  # Needed for AbstractUser

    def __str__(self):
        return f"{self.tr_number} ({self.role})"
