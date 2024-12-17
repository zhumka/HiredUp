from django.db import models
from django.utils import timezone

# Класс категорий профессий
class JobCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название категории профессий')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')

    def __str__(self):
        return self.name

# Класс профессий
class Profession(models.Model):
    name = models.CharField(max_length=70, unique=True, verbose_name='Название профессии')
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE, related_name='professions', verbose_name='Категория')

    def __str__(self):
        return self.name

# Класс вакансий
class Vacancy(models.Model):  # Исправил опечатку с 'Vacansy'
    JOB_TYPES = [
        ('full_time', 'Полный рабочий день'),
        ('part_time', 'Неполный рабочий день'),
        ('contract', 'Контракт'),
        ('internship', 'Стажировка'),
    ]

    employer = models.ForeignKey('users.EmployerProfile', on_delete=models.CASCADE, verbose_name='Работодатель')
    title = models.CharField(max_length=255, verbose_name='Название вакансии')
    requirements = models.TextField(blank=True, null=True, verbose_name='Описание вакансии')
    responsibilities = models.TextField(blank=True, null=True, verbose_name='Обязанности')  # Исправил 'responsobilities'
    salary_min = models.IntegerField(blank=True, null=True, verbose_name='Минимальная зарплата')
    salary_max = models.IntegerField(blank=True, null=True, verbose_name='Максимальная зарплата')
    experience_required = models.IntegerField(blank=True, null=True, verbose_name='Требуемый опыт работы (в годах)')
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE, related_name='vacancies', verbose_name='Профессия')  # Связь с Profession
    category = models.ForeignKey(JobCategory, on_delete=models.RESTRICT, verbose_name='Категория профессии')
    location = models.CharField(max_length=255, blank=True, null=True, verbose_name='Место работы')
    is_active = models.BooleanField(default=True, verbose_name='Статус вакансии')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    job_type = models.CharField(max_length=20, choices=JOB_TYPES, verbose_name='Тип занятости')

    def __str__(self):
        return self.title

class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('reviewed', 'Рассмотрено'),
        ('accepted', 'Принято'),
        ('rejected', 'Отклонено'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def get_status_css_class(self):
        return {
            'pending': 'status pending',
            'reviewed': 'status reviewed',
            'accepted': 'status accepted',
            'rejected': 'status rejected',
        }.get(self.status, 'status')

    vacancy = models.ForeignKey(
        'work.Vacancy',
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name='Вакансия'
    )
    job_seeker = models.ForeignKey(
        'users.JobSeekerProfile',
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name='Соискатель'
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата подачи'
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус отклика')

    def __str__(self):
        return f"Application: {self.job_seeker.user.username} to {self.vacancy.title}"
