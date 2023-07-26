from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse, Http404
from company.models import*
from employee_account.models import*
from.models import*
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
import random
from django.core.mail import send_mail
from custom_admin.models import UserOTP
from django.db.models import Count
# Create your views here.

def home(request):
        
    return render(request,'admin/home.html')



def admin_login(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        try:
            if user.is_staff:
                login(request,user)
                return redirect('admin_panel')
        except user.DoesNotExist:
            raise Http404('Not authorized staff')

    
    return render(request,'admin/admin_login.html')


def admin_signout(request):
    logout(request)
    return redirect('signin')



@login_required(login_url='admin_login')
def admin_panel(request):
    company = Company.objects.all()
    employee = Employee.objects.all()
    context = {
        'company':company,
        'employee':employee
    }
    return render(request,'admin/admin_panel.html',context)

@login_required(login_url='signin')
def all_recruiters(request):
    recruiters = Company.objects.all()
    context ={
        'recruiters':recruiters
    }
    return render(request,'admin/all_recruiter.html',context)



@login_required(login_url='admin_login')
def delete_recruiter(request,id):
    recruiter = Company.objects.get(id = id)
    recruiter.delete()
    return redirect('all_recruiters')

@login_required(login_url='admin_login')
def pending_recruiter(request):
    recruiter = Company.objects.filter(status='pending')
    return render(request,'admin/recruiter_pending.html',{'recruiter':recruiter})


@login_required(login_url='admin_login')
def change_status(request,id):
    recruiter = Company.objects.get(id = id)
    if request.method=='POST':
        status = request.POST.get('status')
        recruiter.status = status
        recruiter.save()
        messages.success(request,'Request Accepted')
    context={
        'recruiter':recruiter
    }
    
    return render(request,'admin/change_status.html',context)


@login_required(login_url='admin_login')
def posted_jobs(request):
    jobs = Job_Vacancy.objects.all()
    return render(request,'admin/posted_jobs.html',{'jobs':jobs})

@login_required(login_url='admin_login')
def delete_job(request,id):
    delete_job = Job_Vacancy.objects.get(id = id)
    delete_job.delete()
    return redirect('posted_jobs')


#employee-users-details

@login_required(login_url='admin_login')
def all_employee(request):
    employee = Employee.objects.all()
    context ={
        'employee':employee
    }
    return render(request,'admin/all_employee.html',context)

@login_required(login_url='admin_login')
def delete_employee(request,id):
    employee = Employee.objects.get(id = id)
    employee.delete()
    return redirect('all_employee')


#chart representation

class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["January", "February", "March", "April", "May", "June", "July"]

    def get_providers(self):
        """Return names of datasets."""
        return ["Employees Applied","Job Vacancy"]

    def get_data(self):
        """Return 3 datasets to plot."""

        # data = [[75, 44, 92, 11, 44, 95, 35],
        #         [41, 92, 18, 3, 73, 87, 92],
        #         [87, 21, 94, 3, 90, 13, 65]]
        
        all_employees_data = []
        all_employees = Employee.objects.annotate(total_applications = Count('job_application'))
        for employee in all_employees:
            all_employees_data.append(employee.total_applications)
        # combine_data = data +[all_employees_data]
        
        total_job_vacancies_data = []
        job_vacancies = Job_Vacancy.objects.annotate(total_vacancies=Count('id'))
        for vacancy in job_vacancies:
            total_job_vacancies_data.append(vacancy.total_vacancies)

       
        combine_data = [all_employees_data, total_job_vacancies_data]        
        return combine_data
    
    
line_chart = TemplateView.as_view(template_name='line_chart.html')
line_chart_json = LineChartJSONView.as_view()


#common password reset and otp
def forgot_password(request):
    if request.method == 'POST':
            username = request.POST.get('email')
            user = get_object_or_404(User, username=username)
            if user:
                email = user.email
                otp_generated = random.randrange(1000,9999)
                subject = 'password reset'
                message = f'One Time password (OTP) - {otp_generated}'
                from_email = 'belfegor6x@gmail.com'
                to = [email]
                
                send_mail(
                    subject = subject,
                    message = message,
                    from_email = from_email,
                    recipient_list = to,
                    fail_silently = False                    
                )
                UserOTP.objects.update_or_create(
                    user = user,
                    defaults = {'otp':otp_generated}
                )
                messages.success(request, 'Please check your email to reset your password')
                return redirect('otp_verify',username)
            messages.error(request,'invalid user')
    return render(request, 'admin/forgot_password.html')


def otp_verify(request, username):
    user = User.objects.get(username = username)
    if request.method == 'POST':
        otp_obj = UserOTP.objects.get(user = user)
        otp = request.POST.get('otp')
        
        if otp == otp_obj.otp:
            messages.success(request,'OTP verified')
            return redirect('change_password',username)
        messages.error(request,'invalid OTP')
    return render(request,'admin/otp_verify.html',{'email':user.email})

def password_reset(request,username):
    user = User.objects.get(username = username)
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            user.set_password(password1)
            user.save()
            messages.success(request,'password changed')
            return redirect('signin')
        messages.error(request,'invalid password')
        
    return render(request,'admin/password_reset.html')    