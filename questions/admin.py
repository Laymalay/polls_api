from django.contrib import admin
from questions.models import Question, Choice, AnsweredQuestion


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'id']


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'id']


admin.site.register(Question, QuestionAdmin)
admin.site.register(AnsweredQuestion)
admin.site.register(Choice, ChoiceAdmin)
