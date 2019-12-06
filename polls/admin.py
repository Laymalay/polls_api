from django.contrib import admin
from .models import Poll, PassedPoll
from questions.models import Question


class QuestionInLine(admin.TabularInline):
    model = Question
    extra = 0


class PollAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'creator', '_questions']
    inlines = [
        QuestionInLine
    ]

    def _questions(self, obj):
        return obj.questions.all().count()


admin.site.register(Poll, PollAdmin)
admin.site.register(PassedPoll)
