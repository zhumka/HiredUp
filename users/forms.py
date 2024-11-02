from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

User=get_user_model()

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model=User
        fields=['username','email','password1','password2']

    def clean_email(self):
        email=self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Аккаунт с данным адресом электронной почты уже существует!')
        return email

