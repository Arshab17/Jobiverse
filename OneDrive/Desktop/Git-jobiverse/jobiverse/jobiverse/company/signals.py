from django.http import request
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Company, Job_Vacancy, Job_Application,Notification
from django.contrib import messages

# User = get_user_model()
# #notification
# @receiver(post_save, sender=Job_Application)
# def create_job_application_notification(sender, instance, created, request, **kwargs):
#     if created:
#         employee = instance.employee
#         job_vacancy = instance.job_vacancy
#         company = job_vacancy.company
#         message = f"{employee.user.first_name} has applied for {job_vacancy.designation} positon at {company.company_name}"
#         request_user = {
#             'username': request.user.username,
#             'email': request.user.email,
#         }
#         message.add_message(request_user, messages.SUCCESS, message)
@receiver(post_save, sender=Job_Application)
def create_notification(sender, instance, created, **kwargs):
    print('notification test')
    if created:
        print('notification test')
        employee = instance.employee
        job_vacancy = instance.job_vacancy
        message = f"Recieved a job application for {job_vacancy.designation}"
        Notification.objects.create(employee=employee, job_vacancy=job_vacancy, message=message)
