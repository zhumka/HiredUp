from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from users.models import EmployerProfile, JobSeekerProfile, Resume
from work.models import JobCategory

User = get_user_model()



# Форма регистрации
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': ''
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': ''
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': ''
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': ''
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # Функции обработки ошибки, если такой емейл уже существует.
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Аккаунт с данным адресом электронной почты уже существует!')
        return email


# Форма для страницы редактирования профиля работодателя.
class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = ['company_name', 'company_description', 'company_address', 'company_logo']


from django import forms
from .models import JobSeekerProfile


# Форма для редактирования профиля соискателя.
class JobSeekerProfileForm(forms.ModelForm):
    # Это вытаскивание полей из модельки юзера.
    username = forms.CharField(
        label="Имя пользователя",
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Введите имя пользователя'})
    )
    first_name = forms.CharField(
        label="Имя",
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Введите свое имя'})
    )
    last_name = forms.CharField(
        label="Фамилия",
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Введите свою фамилию'})
    )
    # Вытаскивание поля категории
    category = forms.ModelChoiceField(queryset=JobCategory.objects.all(), required=False, label="Категория")

    class Meta:
        model = JobSeekerProfile
        fields = ['username', 'first_name', 'last_name', 'category', 'status', 'experience', 'profession']
        widgets = {
            'status': forms.RadioSelect(choices=[(True, 'Ищу работу'), (False, 'Не ищу работу')]),
            'experience': forms.TextInput(attrs={'placeholder': 'Введите опыт работы в годах'}),
            'profession': forms.Select(attrs={'placeholder': 'Выберите профессию'}),
        }

    # Функция инициализации полей юзера и добавление их в БД.
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(JobSeekerProfileForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['username'].initial = user.username
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name

    # Функция сохранения измененных данных(Нужна так как тут идет изменение сразу 2 таблиц User и JobSeekerProfile)
    def save(self, commit=True):
        profile = super(JobSeekerProfileForm, self).save(commit=False)
        user = profile.user

        # Сохраняем поля пользователя
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            profile.save()
        return profile

    # Функция проверки правильности написания опыта работы
    def clean_experience(self):
        experience = self.cleaned_data.get('experience')
        if experience:
            if experience < 0:
                raise ValidationError("Опыт работы не может быть меньше 0 лет")
            if experience > 50:
                raise ValidationError("Опыт работы не может быть больше 50 лет")
        return experience


# Форма для редактирования резюме
class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['education', 'summary', 'skills', 'languages']
