from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserType, EmployerProfile, Resume, JobSeekerProfile

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

# Регистрация моделей с кастомными админ-классами
admin.site.register(UserType, UserTypeAdmin)
admin.site.register(EmployerProfile, EmployerProfileAdmin)
admin.site.register(Resume, ResumeAdmin)
admin.site.register(JobSeekerProfile, JobSeekerProfileAdmin)
