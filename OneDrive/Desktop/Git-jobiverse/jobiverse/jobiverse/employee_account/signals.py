# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from company.models import Notification,Job_Application


# @receiver(post_save, sender=Job_Application)
# def create_notification(sender, instance, created, **kwargs):
#     print('notification emp')
#     if created:
#         print('notification emp')
#         employee = instance.employee
#         job_vacancy = instance.job_vacancy
#         message = f"{job_vacancy} you have applied {Job_Application.status} by {job_vacancy.company}"
#         Notification.objects.create(employee=employee, job_vacancy=job_vacancy, message=message)
    
