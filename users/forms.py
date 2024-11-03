from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from users.models import EmployerProfile, JobSeekerProfile, Resume

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

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = ['company_name', 'company_description', 'company_address', 'company_logo']

class JobSeekerProfileForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ['status', 'experience', 'profession']

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['education', 'summary', 'skills', 'experience', 'languages']