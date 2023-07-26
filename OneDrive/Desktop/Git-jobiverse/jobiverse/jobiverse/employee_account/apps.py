from django.apps import AppConfig


class EmployeeAccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'employee_account'

    def ready(self):
        import employee_account.signals
