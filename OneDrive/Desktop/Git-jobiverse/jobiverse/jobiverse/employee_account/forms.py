# from django import forms
# from django.core.exceptions import ValidationError
# from .models import Employee
# from django.forms import ModelForm
from django import forms
from company.models import Job_Application

# class EmployeeForm(ModelForm):

#     class Meta:
#         model = Employee
#         fields = ['user','email','DOB','profile_img','resume','phone']
        
      
        
#     # Add custom validation for email field
#     def clean_email(self):
#         email = self.cleaned_data['email']
#         if Employee.objects.filter(email=email).exists():
#             raise forms.ValidationError("This email address is already in use.")
#         return email




class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = Job_Application
        fields = [ 'resume', 'cover_letter']
        exclude = ['designation','status']
        

        widgets = {
        #     'job_vacancy': forms.Select(attrs={'class': 'form-control'}),
             'resume': forms.FileInput(attrs={'class': 'form-control'}),
            'cover_letter': forms.Textarea(attrs={'class': 'form-control'})
        #     'status': forms.Select(attrs={'class': 'form-control'}),
         }
