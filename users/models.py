from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    about = models.TextField(max_length=500, blank=True)
    avatar_key = models.TextField(null=True, max_length=300)
    avatar = models.TextField(null=True, max_length=300)
    
    def __str__(self):
        return self.username