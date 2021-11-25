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
        "question_answered": False,
        "next_question": None
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