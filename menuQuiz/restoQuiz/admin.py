from django.contrib import admin

from .models import Question, Choice, User

class ChoiceAdmin(admin.ModelAdmin):
    fields = ['id', 'question', 'choice_text', 'is_correct_answer']
    list_display = ('id', 'question', 'choice_text', 'is_correct_answer')

class UserAdmin(admin.ModelAdmin):
    fields = ['email', 'name', 'is_superuser', 'creation_date']
    list_display = ('email', 'name', 'is_superuser', 'creation_date')

admin.site.register(Question)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(User, UserAdmin)
