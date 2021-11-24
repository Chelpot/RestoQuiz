from django.urls import path

from . import views

app_name = 'restoQuiz'
urlpatterns = [
    path('', views.index, name='index'),
    path('question/<int:question_id>/', views.detail, name='detail'),
    path('launch_quiz/<int:quiz_id>/', views.launch_quiz, name='launch_quiz'),
]