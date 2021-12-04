from datetime import *

from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Question, Choice, User, SessionQuiz, MenuQuiz
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.template.defaultfilters import register
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q

from .forms import SignUpForm

# Create your views here.
def index(request):

    current_menu_quiz = MenuQuiz.objects.filter(pk=1)[0]
    print(current_menu_quiz)

    latest_question_list = Question.objects.filter(associated_quiz=current_menu_quiz)
    print(latest_question_list)
    user = request.user
    if not user.is_authenticated:
        context = {"question_list": latest_question_list,
                   "menus": current_menu_quiz,}
        return render(request, 'restoQuiz/index.html', context)

    # if request.method == 'POST':
    #
    #     session = SessionQuiz.objects.filter(user=user, menu=current_menu_quiz)
    #     #We want only one session per user and quiz
    #     if session:
    #         session.delete()
    #
    #     session = SessionQuiz(user=user, menu=current_menu_quiz, current_question_index=0, current_number_good_answer=0 )
    #     session.add_questions(latest_question_list)
    #     session.save()
    #
    #
    #     return detail(request,
    #                     question_id=session.list_of_questions[0].id,
    #                     menu_id=current_menu_quiz.id)

    context = {"question_list": latest_question_list,
                   "menus": current_menu_quiz,}
    return render(request, 'restoQuiz/index.html', context)

def detail(request, question_id, menu_id):

    message = "propriété GET : {} et requête : {}".format(question_id, menu_id)

    question = get_object_or_404(Question, pk=question_id)
    choices = Choice.objects.filter(question=question)
    context = {
        "question": question,
        "choices": choices,
        "question_answered": False,
        "next_question": None,
        "number_good_answer": 0,
        "menu_id": menu_id,
               }
    if Question.objects.filter(pk=question_id).exists():
        context.update({"next_question": question_id + 1})
        print(question_id)

    if request.method == 'POST':
        buttons_states_list=[]
        dict_recap_answer={}

        are_answers_correct = True
        for i in range(0, len(choices)):
            #get checkbox state from html
            state = request.POST.get('btn-check-{}'.format(i))
            buttons_states_list.append(state)

            #Check if correct answer
            if ((choices[i].is_correct_answer and not state) or (not choices[i].is_correct_answer and state=="on")):
                answer = {choices[i]: "Mauvaise réponse",}
                are_answers_correct = False
            else:
                answer = {choices[i]: "Bonne réponse",}
            dict_recap_answer.update(answer)

        context.update({
            'all_good': are_answers_correct,
            'recap_answers': dict_recap_answer,
            'question_answered': True,
        })

    return render(request, 'restoQuiz/question.html', context)

def launch_quiz(request, quiz_id):


    return render(request, 'restoQuiz/launch_quiz.html')















@csrf_exempt
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='restoQuiz.auth.CheckPasswordBackend')
            user.is_staff = False
            user.is_superuser = False
            user.creation_date = datetime.now(timezone.utc)
            user.save()

            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@csrf_exempt
def login_user(request):
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')
    return render(request, template_name='registration/login.html')

