from contextlib import nullcontext
from operator import truediv

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.template.context_processors import static
from django.utils import timezone
from work.models import Profession


#Класс пользователей
class User(models.Model):
    USER_TYPES = [
        ('admin', 'Admin'),
        ('employer', 'Employer'),
        ('job_seeker', 'Job Seeker'),
        ('moderation','Moderation'),
    ]

    username = models.CharField(verbose_name='ФИО', max_length=150, unique=True)
    phone_number = models.CharField(verbose_name='Номер телефона', max_length=15, unique=True, blank=True, null=True)
    email = models.EmailField(verbose_name='Почта', max_length=255, unique=True, blank=True, null=True)
    password = models.CharField(verbose_name='Пароль', max_length=255)
    user_type = models.CharField(verbose_name='Тип пользователя', max_length=20, choices=USER_TYPES, default='job_seeker')
    created_at = models.DateTimeField('Дата создания', default=timezone.now)

    def __str__(self):
        return self.username

#Класс для профилей работодателей
class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(verbose_name='Имя компании', max_length=255, blank=True, null=True)
    company_description = models.TextField(verbose_name='Описание компании',blank=True, null=True)
    company_address = models.CharField(verbose_name='Адрес компании', max_length=255, blank=True, null=True)
    company_logo=models.ImageField(upload_to='work/static/users/img',default='Изображение отсутствует')
    created_at = models.DateTimeField('Дата создания', default=timezone.now)

    def __str__(self):
        return self.company_name if self.company_name else f"Employer {self.user.username}"






#Класс для резюме
class Resume(models.Model):
    EDUCATION_CHOICES = [
        ('none', 'Без образования'),  # Новый вариант
        ('school', 'Школьное образование'),  # Новый вариант
        ('bachelor', 'Бакалавр'),
        ('master', 'Магистр'),
        ('phd', 'Аспирант'),
        ('doctorate', 'Доктор наук'),
    ]
    education = models.CharField(max_length=20, choices=EDUCATION_CHOICES)
    summary = models.TextField(blank=True, null=True, verbose_name='Общий текст резюме')
    skills = models.TextField(blank=True, null=True, verbose_name='Навыки')
    experience = models.TextField(blank=True, null=True, verbose_name='Опыт работы(в годах)')
    languages = models.TextField(blank=True, null=True, verbose_name='Знание языков')
    file=models.FileField(upload_to='static/users/resumes',null=True,blank=True)
    created_at = models.DateTimeField('Дата создания', default=timezone.now)


    def __str__(self):
        return f"Resume {self.id}"

#Класс для профиля соискателей работы
class JobSeekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.SET_NULL, null=True, blank=True)
    experience = models.PositiveIntegerField(
        verbose_name="Опыт работы (в годах)",
        validators=[
            MinValueValidator(0, message="Опыт работы не может быть меньше 0 лет"),
            MaxValueValidator(50, message="Опыт работы не может быть больше 50 лет")
        ],
        help_text="Введите количество лет опыта (от 0 до 50)",
        blank = True,
        null = True
    )
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE, related_name='job_seekers')
    created_at = models.DateTimeField('Дата создания', default=timezone.now)
    status=models.BooleanField(default=False)

    def __str__(self):
        return f"Job Seeker {self.user.username}"

