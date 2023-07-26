from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from.models import Employee
# from custom_admin.models import User
# from.forms import EmployeeForm
# Register your models here.



# fields = list(UserAdmin.fieldsets)
# fields[1] = ('personal info',{'fields':('first_name','last_name','email','DOB','resume','profile_img')})
# UserAdmin.fieldsets = tuple(fields)

# admin.site.register(Employee,UserAdmin)


admin.site.register(Employee)
