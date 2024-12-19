from django.contrib import admin
from .models import JobCategory, Profession, Vacancy
import csv
from django.http import HttpResponse


def export_statistics(modeladmin, request, queryset):
    """
    Экспорт статистики по вакансиям в CSV.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="statistics.csv"'
    response.write('\ufeff'.encode('utf-8'))

    writer = csv.writer(response)
    writer.writerow(['Всего вакансий', 'Активные вакансии', 'Неактивные вакансии',
                     'Всего профессий', 'Всего категорий'])

    total_vacancies = Vacancy.objects.count()
    active_vacancies = Vacancy.objects.filter(is_active=True).count()
    inactive_vacancies = Vacancy.objects.filter(is_active=False).count()
    total_professions = Profession.objects.count()
    total_categories = JobCategory.objects.count()

    writer.writerow([total_vacancies, active_vacancies, inactive_vacancies,
                     total_professions, total_categories])

    return response


export_statistics.short_description = "Экспорт статистики в CSV"


# Настройка админ-класса для JobCategory
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)
    list_filter = ('created_at',)

# Настройка админ-класса для Profession
class ProfessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name',)
    ordering = ('name',)
    list_filter = ('category',)

# Настройка админ-класса для Vacancy
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer', 'salary_min', 'salary_max', 'job_type', 'is_active', 'created_at')
    search_fields = ('title', 'employer__user__username')  # Поиск по названию и имени пользователя работодателя
    ordering = ('created_at',)
    list_filter = ('job_type', 'is_active', 'category', 'profession')
    actions = [export_statistics]

    def salary_range(self, obj):
        return f"{obj.salary_min} - {obj.salary_max} руб." if obj.salary_min and obj.salary_max else "Не указана"
    salary_range.short_description = 'Диапазон зарплаты'  # Название столбца

# Регистрация моделей с кастомными админ-классами
admin.site.register(JobCategory, JobCategoryAdmin)
admin.site.register(Profession, ProfessionAdmin)
admin.site.register(Vacancy, VacancyAdmin)




