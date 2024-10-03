from django.db import models
from django.db import models
from django.utils import timezone
from users.models import EmployerProfile

#Класс категорий профессий
class JobCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название профессии')
    description = models.TextField(blank=True, null=True, verbose_name='Описание професии')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    updated_at = models.DateTimeField(default=timezone.now, verbose_name='Дата обновления')

    def __str__(self):
        return self.name

#Класс вакансий
class Job(models.Model):
    employer = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE, verbose_name='Работодатель')
    title = models.CharField(max_length=255, verbose_name='Название вакансии')
    description = models.TextField(blank=True, null=True, verbose_name='Описание вакансии')
    salary_min = models.IntegerField(blank=True, null=True, verbose_name='Минимальная зарплата')
    salary_max = models.IntegerField(blank=True, null=True, verbose_name='Максимальная зарплата')
    experience_required = models.IntegerField(blank=True, null=True, verbose_name='Требуемый опыт работы')
    profession = models.CharField(max_length=100, blank=True, null=True, verbose_name='Профессия')
    category = models.ForeignKey(JobCategory, on_delete=models.RESTRICT, verbose_name='Категория профессии')
    location = models.CharField(max_length=255, blank=True, null=True, verbose_name='Место работы')
    is_active = models.BooleanField(default=True, verbose_name='Статус вакансии')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    updated_at = models.DateTimeField(default=timezone.now, verbose_name='Дата обновления')

    def __str__(self):
        return self.title
