from django.contrib import admin

from .models import Question, Choice

class ChoiceAdmin(admin.ModelAdmin):
    fields = ['question', 'choice_text', 'is_correct_answer']
    list_display = ('question', 'choice_text', 'is_correct_answer')


admin.site.register(Question)
admin.site.register(Choice, ChoiceAdmin)