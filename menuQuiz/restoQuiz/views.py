from django.shortcuts import render, get_object_or_404
from .models import Question, Choice

# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')
    context = {"question_list": latest_question_list}
    return render(request, 'restoQuiz/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = Choice.objects.filter(question=question)
    context = {
        "question": question,
        "choices": choices,
               }

    return render(request, 'restoQuiz/question.html', context)

def launch_quiz(request, quiz_id):


    return render(request, 'restoQuiz/launch_quiz.html')