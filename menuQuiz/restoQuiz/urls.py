from django.urls import include, path, re_path

from . import views

app_name = 'restoQuiz'
urlpatterns = [
    path('', views.index, name='index'),
    path(r'detail/<int:question_id>/<int:menu_id>/', views.detail, name='detail'),
    path('launch_quiz/<int:quiz_id>/', views.launch_quiz, name='launch_quiz'),
    path(r'recap/<int:score>/<int:nb_questions>/', views.recap, name='recap'),
    re_path(r"^auth/", include("restoQuiz.auth")),
    re_path(r'^login_user/$', views.login_user, name='login_user'),
    path('signup/', views.signup, name='signup'),

]