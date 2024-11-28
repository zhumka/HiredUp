# Generated by Django 5.1.1 on 2024-11-28 08:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_resume_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobseekerprofile',
            name='experience',
        ),
        migrations.AddField(
            model_name='jobseekerprofile',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, verbose_name='Дата рождения'),
        ),
        migrations.AddField(
            model_name='jobseekerprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator('^\\+?1?\\d{9,15}$', message='Введите корректный номер телефона')], verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='resume',
            name='experience',
            field=models.PositiveIntegerField(blank=True, help_text='Введите количество лет опыта (от 0 до 50)', null=True, validators=[django.core.validators.MinValueValidator(0, message='Опыт работы не может быть меньше 0 лет'), django.core.validators.MaxValueValidator(50, message='Опыт работы не может быть больше 50 лет')], verbose_name='Опыт работы (в годах)'),
        ),
    ]
