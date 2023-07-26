from django.urls import path
from . import views
from .views import line_chart, line_chart_json

urlpatterns = [
    path('', views.home, name='home_admin'),
    # path('',views.form_view,name='form_view'),

    path('custom_admin/login/',views.admin_login,name='admin_login'),
    path('custom_admin/signout/',views.admin_signout,name='admin_signout'),
    path('new_admin/home/',views.admin_panel,name='admin_panel'),

    path('all/recruiters/',views.all_recruiters,name='all_recruiters'),
    path('delete_recruiter/<int:id>/',views.delete_recruiter,name='delete_recruiter'),
    path('pending_request/recruiter',views.pending_recruiter,name="pending_recruiter"),
    path('change_status/<int:id>',views.change_status,name='change_status'),
    path('jobs/posted/',views.posted_jobs,name='posted_jobs'),
    path('delete/job/<int:id>/',views.delete_job,name='delete_job'),

    path('all/employee/',views.all_employee,name='all_employee'),
    path('delete/employee/<int:id>/',views.delete_employee,name='delete_employee'),

    path('chart',views.line_chart, name='line_chart'),
    path('chartJSON', views.line_chart_json, name='line_chart_json'),
    
    path('forgot/password/',views.forgot_password,name="forgot_password"),
    path('otp/verificatio/<str:username>/',views.otp_verify,name='otp_verify'),
    path('reset/password/<str:username>/',views.password_reset,name='change_password')
]


