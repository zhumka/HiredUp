from django.contrib.auth.models import User  # Базовая модель пользователя Django
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from django.utils import timezone
from work.models import Profession


# Класс для хранения типов пользователей
class UserType(models.Model):
    USER_TYPES = [
        ('admin', 'Admin'),
        ('employer', 'Employer'),
        ('job_seeker', 'Job Seeker'),
        ('moderator', 'Moderator'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_type')
    user_type = models.CharField(verbose_name='Тип пользователя', max_length=20, choices=USER_TYPES)

    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"

# Класс для профиля работодателей
class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(verbose_name='Имя компании', max_length=255, blank=True, null=True)
    company_description = models.TextField(verbose_name='Описание компании', blank=True, null=True)
    company_address = models.CharField(verbose_name='Адрес компании', max_length=255, blank=True, null=True)
    company_logo = models.ImageField(upload_to='users/static/users/img', default='users/static/users/img/defaultCompanyAvatar.svg')
    created_at = models.DateTimeField('Дата создания', default=timezone.now)

    def __str__(self):
        return self.company_name if self.company_name else f"Employer {self.user.username}"

# Класс для резюме
class Resume(models.Model):
    job_seeker_profile = models.ForeignKey('JobSeekerProfile', on_delete=models.CASCADE, related_name='resumes', default=None)
    EDUCATION_CHOICES = [
        ('none', 'Без образования'),
        ('school', 'Школьное образование'),
        ('bachelor', 'Бакалавр'),
        ('master', 'Магистр'),
        ('phd', 'Аспирант'),
        ('doctorate', 'Доктор наук'),
    ]
    education = models.CharField(max_length=20, choices=EDUCATION_CHOICES)
    summary = models.TextField(blank=True, null=True, verbose_name='Общий текст резюме')
    skills = models.TextField(blank=True, null=True, verbose_name='Навыки')
    experience = models.PositiveIntegerField(
        verbose_name="Опыт работы (в годах)",
        validators=[
            MinValueValidator(0, message="Опыт работы не может быть меньше 0 лет"),
            MaxValueValidator(50, message="Опыт работы не может быть больше 50 лет")
        ],
        help_text="Введите количество лет опыта (от 0 до 50)",
        blank=True,
        null=True
    )
    languages = models.TextField(blank=True, null=True, verbose_name='Знание языков')
    file = models.FileField(upload_to='users/static/users/resumes', null=True, blank=True)
    created_at = models.DateTimeField('Дата создания', default=timezone.now)

    def __str__(self):
        return f"Resume {self.id} - {self.job_seeker_profile.user.username}"

# Класс для профиля соискателей работы
class JobSeekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='job_seeker_profile')
    resume = models.OneToOneField(Resume, on_delete=models.SET_NULL, null=True, blank=True)
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE, related_name='job_seekers', null=True, blank=True)
    created_at = models.DateTimeField('Дата создания', default=timezone.now)
    status = models.BooleanField(default=False)
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name='Номер телефона',
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', message="Введите корректный номер телефона")]
    )  # Новое поле для телефона
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата рождения'
    )  # Новое поле для даты рождения
    avatar = models.ImageField(
        upload_to='users/static/users/img',  # Папка для сохранения изображений
        default='users/static/users/img/defaultUserAvatar.svg',  # Значение по умолчанию
        blank=True,
        null=True,
        verbose_name='Аватар'
    )  # Новое поле для аватара

    def __str__(self):
        return f"Job Seeker {self.user.username}"
