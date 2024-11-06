from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from users.models import EmployerProfile, JobSeekerProfile, Resume
from work.models import JobCategory

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

from django import forms
from .models import JobSeekerProfile

class JobSeekerProfileForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=JobCategory.objects.all(), required=False, label="Категория")
    class Meta:
        model = JobSeekerProfile
        fields = ['category' ,'status', 'experience', 'profession']
        widgets = {
            'status': forms.RadioSelect(choices=[(True, 'Ищу работу'), (False, 'Не ищу работу')]),
        }


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['education', 'summary', 'skills', 'languages']