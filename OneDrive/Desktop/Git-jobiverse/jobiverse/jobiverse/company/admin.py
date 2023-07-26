from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from.models import Company,Job_Application,Job_Vacancy
from custom_admin.models import User
# Register your models here.
admin.site.register(Company)
admin.site.register(Job_Vacancy)
admin.site.register(Job_Application)