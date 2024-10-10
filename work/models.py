from idlelib.pyparse import trans

from django.db import models
from django.db import models
from django.db.models import ForeignKey
from django.utils import timezone


#Класс категорий профессий
class JobCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название профессии')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')


    def __str__(self):
        return self.name

class Profession(models.Model):
    name=models.CharField(max_length=70,unique=True)
    category=models.ForeignKey(JobCategory,on_delete=models.CASCADE,related_name='Профессия')

#Класс вакансий
class Vacansy(models.Model):
    JOB_TYPES = [
        ('full_time', 'Полный рабочий день'),
        ('part_time', 'Неполный рабочий день'),
        ('contract', 'Контракт'),
        ('internship', 'Стажировка'),
    ]
    employer = models.ForeignKey('users.EmployerProfile', on_delete=models.CASCADE, verbose_name='Работодатель')
    title = models.CharField(max_length=255, verbose_name='Название вакансии')
    requirements= models.TextField(blank=True, null=True, verbose_name='Описание вакансии')
    responsobilities=models.TextField(blank=True,null=True)
    salary_min = models.IntegerField(blank=True, null=True, verbose_name='Минимальная зарплата')
    salary_max = models.IntegerField(blank=True, null=True, verbose_name='Максимальная зарплата')
    experience_required = models.IntegerField(blank=True, null=True, verbose_name='Требуемый опыт работы')
    profession = models.CharField(max_length=100, blank=True, null=True, verbose_name='Профессия')
    category = models.ForeignKey(JobCategory, on_delete=models.RESTRICT, verbose_name='Категория профессии')
    location = models.CharField(max_length=255, blank=True, null=True, verbose_name='Место работы')
    is_active = models.BooleanField(default=True, verbose_name='Статус вакансии')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    job_type = models.CharField(max_length=20, choices=JOB_TYPES)


    def __str__(self):
        return self.title
