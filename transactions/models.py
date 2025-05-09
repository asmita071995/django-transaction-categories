from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

class RawTransaction(models.Model):
    raw_data = models.TextField()

    def __str__(self):
        return f"RawTransaction {self.id}"