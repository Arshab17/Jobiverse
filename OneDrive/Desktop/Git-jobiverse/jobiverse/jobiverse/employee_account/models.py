from django.contrib.auth.models import AbstractUser
from django.db import models
from custom_admin.models import User
# from django.contrib.auth.models import User

# class EmployeeManager(models.Manager):
#     def create_user(self,email, first_name, last_name, password, DOB=None, profile_img=None, resume=None, phone=None):
#         # Create a new user instance
#         user = User(email=email, first_name=first_name, last_name=last_name)
#         user.set_password(password)
#         user.save(using=self._db)

#         # Create an employee instance
#         employee = self.model(user=user, email=email, DOB=DOB, profile_img=profile_img, resume=resume, phone=phone)
#         employee.save(using=self._db)
#         return employee

class Employee(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    email = models.EmailField(unique=True,max_length=250)
    DOB = models.CharField(max_length=10,null=True,blank=True)
    profile_img = models.ImageField(upload_to='employee_img/',null=True,blank=True)
    resume = models.FileField(upload_to='resume_employee/',null=True,blank=True)
    phone = models.CharField(max_length=20)
    

    # objects = EmployeeManager()

    def __str__(self):
        return self.email




class ProfileDetails(models.Model):
    user = models.ForeignKey(Employee, on_delete=models.CASCADE,related_name='profile')
    profile_img = models.FileField(upload_to='employee_img/', null=True, blank=True)
    about = models.CharField(max_length=250, null=True, blank=True)
    hobbies = models.CharField(max_length=250, null=True, blank=True)

    # def __str__(self):
    #     return self.user.first_name


class SkillSet(models.Model):
    profile = models.ForeignKey(ProfileDetails, on_delete=models.CASCADE)
    skill = models.CharField(max_length=250, null=True)


class Experience(models.Model):
    profile = models.ForeignKey(ProfileDetails, on_delete=models.CASCADE)
    position = models.CharField(max_length=250, null=True)
    year_started = models.CharField(max_length=20, null=True)
    year_ended = models.CharField(max_length=20, null=True)
    company = models.CharField(max_length=250, null=True)
    location = models.CharField(max_length=250, null=True)
    description = models.CharField(max_length=250, null=True)


class Education(models.Model):
    profile = models.ForeignKey(ProfileDetails, on_delete=models.CASCADE)
    university_college = models.CharField(max_length=250, null=True)
    year_started = models.CharField(max_length=20, null=True)
    year_ended = models.CharField(max_length=20, null=True)
    course = models.CharField(max_length=250, null=True)


class Project(models.Model):
    profile = models.ForeignKey(ProfileDetails, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=250, null=True)
    project_file = models.FileField(upload_to='employee_project/',null=True)
    description = models.CharField(max_length=250, null=True)
