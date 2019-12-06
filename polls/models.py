from django.db import models
from django.conf import settings


class Poll(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='polls', on_delete=models.CASCADE)
    image_path = models.TextField(max_length=300, null=True)

    def __str__(self):
        """A string representation of the model."""
        return self.title


class PassedPoll(models.Model):
    poll = models.ForeignKey(
        Poll, related_name='passed', on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='passed_polls', on_delete=models.CASCADE)
    score = models.FloatField(null=True)
    
    def __str__(self):
        """A string representation of the model."""
        return f"{self.poll.title} {self.user.username} {self.score}"
