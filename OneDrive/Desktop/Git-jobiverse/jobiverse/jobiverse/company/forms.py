from django import forms
from .models import Job_Application

class JobApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Job_Application
        fields = ['status']



    # def save(self, commit=True):
    #     job_application = super().save(commit=False)
    #     job_application.job_vacancy = self.cleaned_data['job_vacancy']
    #     if commit:
    #         job_application.save()
    #         self.save_m2m()
    #     return job_application     
    