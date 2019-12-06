from django.db import models
from polls.models import Poll,PassedPoll


class Question(models.Model):
    title = models.TextField()
    poll = models.ForeignKey(
        Poll, related_name='questions', on_delete=models.CASCADE)
    answer = models.CharField(max_length=30)

    def __str__(self):
        """A string representation of the model."""
        return self.title


class Choice(models.Model):
    title = models.TextField()
    question = models.ForeignKey(
        Question, related_name='choices', on_delete=models.CASCADE)

    def __str__(self):
        """A string representation of the model."""
        return self.title


class AnsweredQuestion(models.Model):
    question = models.ForeignKey(
        Question, related_name='answered_questions', on_delete=models.CASCADE)
    passed_poll = models.ForeignKey(
        PassedPoll, related_name='answers', on_delete=models.CASCADE)
    choice = models.ForeignKey(
        Choice, related_name='selected_choices', on_delete=models.CASCADE)
    correct = models.BooleanField()

    def __str__(self):
        """A string representation of the model."""
        return f"{self.question.title} - {self.choice.title}"
