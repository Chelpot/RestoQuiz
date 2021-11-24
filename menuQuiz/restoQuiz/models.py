from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=1000, verbose_name='Intitulé de la question')
    pub_date = models.DateTimeField('date de publication')

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Question concernée")
    choice_text = models.CharField(max_length=200, verbose_name="Proposition")
    is_correct_answer = models.BooleanField(default=False, verbose_name="réponse correcte")

    def __str__(self):
        return self.choice_text