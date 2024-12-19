from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserType, EmployerProfile, Resume, JobSeekerProfile

import csv
from django.http import HttpResponse
from work.models import Vacancy, Application


def export_user_statistics(modeladmin, request, queryset):
    """
    Экспорт статистики работодателей или соискателей в CSV.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="user_statistics.csv"'
    response.write('\ufeff'.encode('utf-8'))

    writer = csv.writer(response)
    writer.writerow([
        'Тип пользователя', 'Пользователь', 'Доп. информация',
        'Всего вакансий/откликов', 'Активные/Принятые', 'Неактивные/Отклоненные', 'В ожидании'
    ])

    # Проверяем, к какому классу относится queryset
    if queryset.model == EmployerProfile:
        for employer in queryset:
            total_vacancies = Vacancy.objects.filter(employer=employer).count()
            active_vacancies = Vacancy.objects.filter(employer=employer, is_active=True).count()
            inactive_vacancies = Vacancy.objects.filter(employer=employer, is_active=False).count()

            writer.writerow([
                'Работодатель', employer.user.username, employer.company_name,
                total_vacancies, active_vacancies, inactive_vacancies, 'N/A'
            ])

    elif queryset.model == JobSeekerProfile:
        for job_seeker in queryset:
            total_applications = Application.objects.filter(job_seeker=job_seeker).count()
            accepted = Application.objects.filter(job_seeker=job_seeker, status='accepted').count()
            rejected = Application.objects.filter(job_seeker=job_seeker, status='rejected').count()
            pending = Application.objects.filter(job_seeker=job_seeker, status='pending').count()

            experience = job_seeker.resume.experience if job_seeker.resume else "Не указан"
            writer.writerow([
                'Соискатель', job_seeker.user.username, f"Опыт: {experience}",
                total_applications, accepted, rejected, pending
            ])

    return response



# Настройка админ-класса для UserType
class UserTypeAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type')
    search_fields = ('user__username',)
    ordering = ('user__username',)

# Настройка админ-класса для EmployerProfile
class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'created_at')
    search_fields = ('company_name', 'user__username')
    ordering = ('created_at',)
    list_filter = ('created_at',)
    actions = [export_user_statistics]

# Настройка админ-класса для Resume
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('job_seeker_profile', 'education', 'experience', 'created_at')
    search_fields = ('job_seeker_profile__user__username',)
    ordering = ('created_at',)
    list_filter = ('education',)


# Настройка админ-класса для JobSeekerProfile
class JobSeekerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profession', 'created_at', 'status', 'phone_number', 'date_of_birth', 'avatar')
    search_fields = ('user__username', 'profession__name')
    ordering = ('created_at',)
    list_filter = ('profession', 'status')
    actions = [export_user_statistics]

# Регистрация моделей с кастомными админ-классами
admin.site.register(UserType, UserTypeAdmin)
admin.site.register(EmployerProfile, EmployerProfileAdmin)
admin.site.register(Resume, ResumeAdmin)
admin.site.register(JobSeekerProfile, JobSeekerProfileAdmin)
