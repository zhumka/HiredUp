

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date
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
import datetime

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

    date_of_birth = forms.DateField(
        label="Дата рождения",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'placeholder': 'Выберите дату рождения',
        }),
        required=False
    )

    avatar = forms.ImageField(
        label="Аватарка",
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'style': 'border: 1px solid #ccc; padding: 10px;',
        })
    )

    class Meta:
        model = JobSeekerProfile
        fields = ['username', 'first_name', 'last_name', 'category',
                  'status', 'profession','phone_number', 'date_of_birth', 'avatar']
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

            # Проходим по всем полям формы и устанавливаем начальные значения из экземпляра модели
        for field in self.fields:
            field_value = getattr(self.instance, field, None)
            if field_value is not None:
                # Преобразуем в строку, если это необходимо (например, для дат)
                if isinstance(field_value, datetime.date):
                    field_value = field_value.strftime('%Y-%m-%d')
                self.fields[field].initial = field_value

        profile = kwargs.pop('profile', None)  # Получаем профиль
        if profile:
            self.fields[
                'date_of_birth'].initial = profile.date_of_birth or ''  # устанавливаем пустое значение, если дата не указана
            self.fields['status'].initial = profile.status  # Обратите внимание на это

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth:  # Если дата рождения указана
            # Проверка на возраст 18 лет
            today = date.today()
            age = today.year - date_of_birth.year
            if today.month < date_of_birth.month or (today.month == date_of_birth.month and today.day < date_of_birth.day):
                age -= 1
            if age < 18:
                raise ValidationError("Возраст должен быть не менее 18 лет.")
        # Если дата рождения не указана, возвращаем None (для пустого значения)
        return date_of_birth

    def save(self, commit=True):
        profile = super(JobSeekerProfileForm, self).save(commit=False)
        user = profile.user

        # Сохраняем данные пользователя
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        # Обработка даты рождения
        date_of_birth = self.cleaned_data.get('date_of_birth', None)
        if date_of_birth is not None:
            print(f"Сохраняем дату рождения: {date_of_birth}")  # Отладка
            profile.date_of_birth = date_of_birth
        else:
            print("Дата рождения не передана.")  # Отладка
            # Если дата не была изменена, оставляем текущее значение
            profile.date_of_birth = self.instance.date_of_birth

        if commit:
            user.save()
            profile.save()

        return profile


# Форма для редактирования резюме
class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['education', 'summary', 'skills', 'languages', 'experience']

        # Функция проверки правильности написания опыта работы
        def clean_experience(self):
            experience = self.cleaned_data.get('experience')
            if experience:
                if experience < 0:
                    raise ValidationError("Опыт работы не может быть меньше 0 лет")
                if experience > 50:
                    raise ValidationError("Опыт работы не может быть больше 50 лет")
            return experience
