from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import JobCategory, Vacancy, Profession

from django.contrib import admin
from .models import JobCategory, Profession, Vacancy

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

    def salary_range(self, obj):
        return f"{obj.salary_min} - {obj.salary_max} руб." if obj.salary_min and obj.salary_max else "Не указана"
    salary_range.short_description = 'Диапазон зарплаты'  # Название столбца

# Регистрация моделей с кастомными админ-классами
admin.site.register(JobCategory, JobCategoryAdmin)
admin.site.register(Profession, ProfessionAdmin)
admin.site.register(Vacancy, VacancyAdmin)

