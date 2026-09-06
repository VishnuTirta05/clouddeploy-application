# Create your models here.
from django.db import models


class Deployment(models.Model):
    application = models.CharField(max_length=100)
    version = models.CharField(max_length=50)
    environment = models.CharField(max_length=50)
    status = models.CharField(max_length=30, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.application} - {self.version}"