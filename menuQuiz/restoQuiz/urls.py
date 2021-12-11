from django.urls import include, path, re_path

from . import views

app_name = 'restoQuiz'
urlpatterns = [
    path('', views.index, name='index'),
    path(r'detail/<int:question_id>/<int:menu_id>/', views.detail, name='detail'),
    path('results/', views.results, name='results'),
    path(r'recap/<int:score>/<int:nb_questions>/', views.recap, name='recap'),
    re_path(r"^auth/", include("restoQuiz.auth")),
    re_path(r'^login_user/$', views.login_user, name='login_user'),
    path('signup/', views.signup, name='signup'),

]