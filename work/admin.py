from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import  JobCategory, Vacancy

admin.site.register(JobCategory)
admin.site.register(Vacancy)
