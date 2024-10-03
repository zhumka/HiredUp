from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User,JobSeekerProfile,Resume,EmployerProfile


admin.site.register(User)
admin.site.register(JobSeekerProfile)
admin.site.register(Resume)
admin.site.register(EmployerProfile)
