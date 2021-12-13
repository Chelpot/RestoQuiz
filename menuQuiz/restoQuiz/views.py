from datetime import *

from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Question, Choice, User, SessionQuiz, MenuQuiz, ResultScoreFinal
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.template.defaultfilters import register
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q

from .forms import SignUpForm


def index(request):
    # Todo: Make it better, not raw like this
    current_menu_quiz = MenuQuiz.objects.filter(pk=1)[0]
    latest_question_list = Question.objects.filter(associated_quiz=current_menu_quiz).order_by("id")
    context = {"question_list": latest_question_list,
               "menu": current_menu_quiz, }
    return render(request, 'restoQuiz/index.html', context)


def detail(request, question_id, menu_id):

    if request.user.is_authenticated:
        current_menu_quiz = MenuQuiz.objects.filter(pk=menu_id)[0]

        question_query_set = Question.objects.filter(associated_quiz=current_menu_quiz).order_by('id')
        question = get_object_or_404(Question, pk=question_id)
        question_list = (*question_query_set,)
        is_last_question = len(question_list) - 1 == question_list.index(question)
        if not is_last_question:
            next_question = question_list[question_list.index(question) + 1].id
        else:
            next_question = 0

        choices = Choice.objects.filter(question=question)
        context = {
            "question": question,
            "choices": choices,
            "question_answered": False,
            "next_question": next_question,
            "menu_id": menu_id,
            "is_last_question": is_last_question,
            "nb_questions": len(question_list)
        }

        if request.method == 'POST':
            buttons_states_list = []
            dict_recap_answer = {}

            are_answers_correct = True
            for i in range(0, len(choices)):
                # get checkbox state from html
                state = request.POST.get('btn-check-{}'.format(i))
                buttons_states_list.append(state)

                # Check if correct answer
                if ((choices[i].is_correct_answer and not state) or (not choices[i].is_correct_answer and state == "on")):
                    answer = {choices[i]: "Mauvaise réponse", }
                    are_answers_correct = False
                else:
                    answer = {choices[i]: "Bonne réponse", }
                dict_recap_answer.update(answer)


            result, created = ResultScoreFinal.objects.filter(
                Q(is_final_result=False),
            ).get_or_create(user=request.user, menu=current_menu_quiz)
            result.nb_question = len(question_list)

            if are_answers_correct:
                result.score = result.score + 1
            if is_last_question:
                result.is_final_result = True

            result.save()

            context.update({
                'all_good': are_answers_correct,
                'recap_answers': dict_recap_answer,
                'question_answered': True,
                "score": result.score,
            })
        return render(request, 'restoQuiz/question.html', context)
    return render(request, 'restoQuiz/question.html', context)
    # else:
    #     return render(request, 'registration/must_be_logged_in.html')


def recap(request, score, nb_questions):
    context = {
        "score": score,
        "nb_questions": nb_questions,
    }
    return render(request, 'restoQuiz/recap.html', context=context)

def results(request):
    results_list = (*ResultScoreFinal.objects.order_by("score"),)
    context = {"results": results_list,}
    return render(request, 'restoQuiz/result.html', context)

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
