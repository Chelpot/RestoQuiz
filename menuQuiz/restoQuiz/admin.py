from django.contrib import admin

from .models import Question, Choice, User, MenuQuiz, SessionQuiz

class ChoiceAdmin(admin.ModelAdmin):
    fields = ['question', 'choice_text', 'is_correct_answer']
    list_display = ('question', 'choice_text', 'is_correct_answer')

class UserAdmin(admin.ModelAdmin):
    fields = ['email', 'name', 'is_superuser', 'creation_date']
    list_display = ('email', 'name', 'is_superuser', 'creation_date')

class MenuQuizAdmin(admin.ModelAdmin):
    fields = ['title', 'description']
    list_display = ('title', 'description')

class SessionQuizAdmin(admin.ModelAdmin):
    fields = ['user', 'menu', 'current_question_index', 'current_number_good_answer']
    list_display = ('user', 'menu', 'current_question_index', 'current_number_good_answer')

admin.site.register(Question)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(MenuQuiz, MenuQuizAdmin)
admin.site.register(SessionQuiz, SessionQuizAdmin)
