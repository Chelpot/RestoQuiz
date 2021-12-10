import datetime
import uuid

from django.core.exceptions import ValidationError
from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)







"""
================================================================================
USER PART
================================================================================
"""


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            creation_date=datetime.datetime.now(),
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, password):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=32, blank=False, null=False, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    class Meta:
        app_label = 'restoQuiz'




class MenuQuiz(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre du quiz")
    description = models.CharField(max_length=500, verbose_name="Description")

    def __str__(self):
        return self.title

class Question(models.Model):
    associated_quiz = models.ForeignKey(MenuQuiz, on_delete=models.CASCADE, verbose_name="De quel quiz fait parti cette question ?")
    question_text = models.CharField(max_length=1000, verbose_name='Intitulé de la question')
    pub_date = models.DateTimeField('date de publication', auto_now_add=True)
    answer_text = models.CharField(max_length=2000, verbose_name='Explication de la réponse', default="", blank=True)

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Question concernée")
    choice_text = models.CharField(max_length=200, verbose_name="Proposition")
    is_correct_answer = models.BooleanField(default=False, verbose_name="réponse correcte")

    def __str__(self):
        return self.choice_text


class SessionQuiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur courant")
    menu = models.ForeignKey(MenuQuiz, on_delete=models.CASCADE, verbose_name="Quiz associé")
    creation_date = models.DateTimeField(auto_now_add=True)
    current_question_index = models.IntegerField(blank=True, editable=True, default=0)
    current_number_good_answer = models.IntegerField(default=0, editable=True)

    def add_questions(self, questions):
        self.list_of_questions = questions

    def __str__(self):
        return self.choice_text

class ResultScoreFinal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur")
    menu = models.ForeignKey(MenuQuiz, on_delete=models.CASCADE, verbose_name="Quiz associé")
    score = models.IntegerField(blank=True, editable=True, default=0)
    nb_question = models.IntegerField(blank=True, editable=True, default=0)
    creation_date = models.DateTimeField(auto_now_add=True, editable=True)
    is_final_result = models.BooleanField(default=False, verbose_name="Résultat final (Ne pas toucher)")

    def __str__(self):
        return self.score.__str__()
