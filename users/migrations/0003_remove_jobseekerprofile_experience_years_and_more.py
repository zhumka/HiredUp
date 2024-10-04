# Generated by Django 5.1.1 on 2024-10-03 10:22

import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_job_category_remove_job_employer_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobseekerprofile',
            name='experience_years',
        ),
        migrations.AddField(
            model_name='jobseekerprofile',
            name='experience',
            field=models.PositiveIntegerField(blank=True, help_text='Введите количество лет опыта (от 0 до 50)', null=True, validators=[django.core.validators.MinValueValidator(0, message='Опыт работы не может быть меньше 0 лет'), django.core.validators.MaxValueValidator(50, message='Опыт работы не может быть больше 50 лет')], verbose_name='Опыт работы (в годах)'),
        ),
        migrations.AlterField(
            model_name='employerprofile',
            name='company_address',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Адрес компании'),
        ),
        migrations.AlterField(
            model_name='employerprofile',
            name='company_description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание компании'),
        ),
        migrations.AlterField(
            model_name='employerprofile',
            name='company_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Имя компании'),
        ),
        migrations.AlterField(
            model_name='employerprofile',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='employerprofile',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата обновления'),
        ),
        migrations.AlterField(
            model_name='jobseekerprofile',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='jobseekerprofile',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Город проживания'),
        ),
        migrations.AlterField(
            model_name='jobseekerprofile',
            name='profession',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Профессия'),
        ),
        migrations.AlterField(
            model_name='jobseekerprofile',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата обновления'),
        ),
        migrations.AlterField(
            model_name='resume',
            name='certifications',
            field=models.TextField(blank=True, null=True, verbose_name='Сертификаты'),
        ),
        migrations.AlterField(
            model_name='resume',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='resume',
            name='education',
            field=models.TextField(blank=True, null=True, verbose_name='Образование'),
        ),
        migrations.AlterField(
            model_name='resume',
            name='experience',
            field=models.TextField(blank=True, null=True, verbose_name='Опыт работы(в годах)'),
        ),
        migrations.AlterField(
            model_name='resume',
            name='languages',
            field=models.TextField(blank=True, null=True, verbose_name='Знание языков'),
        ),
        migrations.AlterField(
            model_name='resume',
            name='skills',
            field=models.TextField(blank=True, null=True, verbose_name='Навыки'),
        ),
        migrations.AlterField(
            model_name='resume',
            name='summary',
            field=models.TextField(blank=True, null=True, verbose_name='Общий текст резюме'),
        ),
        migrations.AlterField(
            model_name='resume',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата обновления'),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True, unique=True, verbose_name='Почта'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=255, verbose_name='Пароль'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True, verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата обновления'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('admin', 'Admin'), ('employer', 'Employer'), ('job_seeker', 'Job Seeker')], default='job_seeker', max_length=20, verbose_name='Тип пользователя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True, verbose_name='Никнейм'),
        ),
    ]