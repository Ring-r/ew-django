from django.contrib.auth.models import User
from django.db import models


class SomeEntity(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.user}"
