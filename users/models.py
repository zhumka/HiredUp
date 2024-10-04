from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

#Класс пользователей
class User(models.Model):
    USER_TYPES = [
        ('admin', 'Admin'),
        ('employer', 'Employer'),
        ('job_seeker', 'Job Seeker'),
    ]

    username = models.CharField(verbose_name='Никнейм', max_length=150, unique=True)
    phone_number = models.CharField(verbose_name='Номер телефона', max_length=15, unique=True, blank=True, null=True)
    email = models.EmailField(verbose_name='Почта', max_length=255, unique=True, blank=True, null=True)
    password = models.CharField(verbose_name='Пароль', max_length=255)
    user_type = models.CharField(verbose_name='Тип пользователя', max_length=20, choices=USER_TYPES, default='job_seeker')
    created_at = models.DateTimeField('Дата создания', default=timezone.now)
    updated_at = models.DateTimeField('Дата обновления',default=timezone.now)

    def __str__(self):
        return self.username

#Класс для профилей работодателей
class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(verbose_name='Имя компании', max_length=255, blank=True, null=True)
    company_description = models.TextField(verbose_name='Описание компании',blank=True, null=True)
    company_address = models.CharField(verbose_name='Адрес компании', max_length=255, blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', default=timezone.now)
    updated_at = models.DateTimeField('Дата обновления', default=timezone.now)

    def __str__(self):
        return self.company_name if self.company_name else f"Employer {self.user.username}"






#Класс для резюме
class Resume(models.Model):
    summary = models.TextField(blank=True, null=True, verbose_name='Общий текст резюме')
    skills = models.TextField(blank=True, null=True, verbose_name='Навыки')
    experience = models.TextField(blank=True, null=True, verbose_name='Опыт работы(в годах)')
    education = models.TextField(blank=True, null=True, verbose_name='Образование')
    certifications = models.TextField(blank=True, null=True,verbose_name='Сертификаты')
    languages = models.TextField(blank=True, null=True, verbose_name='Знание языков')
    created_at = models.DateTimeField('Дата создания', default=timezone.now)
    updated_at = models.DateTimeField('Дата обновления', default=timezone.now)
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
    profession = models.CharField(verbose_name='Профессия',max_length=100, blank=True, null=True)
    location = models.CharField(verbose_name='Город проживания',max_length=255, blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', default=timezone.now)
    updated_at = models.DateTimeField('Дата обновления', default=timezone.now)

    def __str__(self):
        return f"Job Seeker {self.user.username}"