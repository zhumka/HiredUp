from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import  JobCategory, Vacansy

admin.site.register(JobCategory)
admin.site.register(Vacansy)
