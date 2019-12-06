from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    about = models.TextField(null=True, max_length=500)

    def __str__(self):
        return self.username