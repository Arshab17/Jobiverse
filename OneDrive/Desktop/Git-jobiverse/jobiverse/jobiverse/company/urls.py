from django.urls import path
from .views import*


urlpatterns = [
    path('company/register/',company_register,name='company_register'),
    path('signin/',sign_in,name='signin'),
    path('signout',company_sign_out,name='company_signout'),
    path('company/home/',home,name='company_home'),
    path('company/profile/',company_profile,name='company_profile'),
    path('company/job-post/',post_a_job,name='job-post'),
    path('company/applicants/',applicant_list,name='applicants_list'),
    path('posted/jobs/',posted_jobs,name='posted_jobs_c'),
    path('live/jobs/',live_jobs,name='live_jobs'),
    path('job-vacancy/<int:id>/status/',publish_or_unpublish,name='publish_or_unpublish'),
    path('job-details/<int:id>/',job_posted_details,name='job_posted_details'),
    path('profile/edit/',profile_edit,name="profile_edit"),
    path('applicant/<int:id>/status/',applicant_status,name="applicant_status"),
    path('edit/post/',edit_post,name="edit_post"),
    path('edit/<int:id>/job_posted/',edit_job_post,name="edit_job_post"),
    path('notification/',notify_on_navbar,name="notification"),
    path('notifiaction/<int:id>/details',notification_details,name='notification_details'),
    path('applicant/<int:id>/profile',applicant_details,name="applicants_profile"),
    path('reset/password/',password_reset,name='reset_password'),
    
    

]