from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Requis')

    class Meta:
        model = User
        fields = ('nom', 'email', 'password1', 'password2', )
