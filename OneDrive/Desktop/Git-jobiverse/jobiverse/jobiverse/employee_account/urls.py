from django.urls import path
from .views import*


urlpatterns = [
    path('register/',register,name='register'), 
    path('signout',sign_out,name='signout'),
    path('edit/profile/',employee_profile_edit,name="emp_edit"),

    path('home',home,name='employee_home'),
    path('job-list/',job_listing,name='job_listing'),
    path('job-details/<int:id>/',job_details,name="job_details"),

    path('profile/',employee_profile,name="employee_profile"),

    path('job_application/<int:id>/create/', job_application_create, name='job_application_create'),
    path('job_application',job_application_detail, name='job_application_detail'),
    
    path('notification/',my_jobs,name='jobs_notification'),
    
    path('add/skill/', add_skill, name='add_skill'),
    path('add/experience/',add_experience,name='add_experience'),
    path('view_resume/<int:profile_id>/',view_resume, name='view_resume'),
    path('add/education/',add_education,name='add_education'),
    path('add/project',add_project,name='add_project'),
    path('edit/<int:id>/experience/',experience_edit,name='experience_edit'),
    
    path('password/employee/reset',password_reset,name="password_reset"),
    path('company/<int:id>/profile/',company_details,name="company_profile"),
    

    

]