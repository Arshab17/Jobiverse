
from django.shortcuts import get_object_or_404, render,redirect
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator
# from company.signals import create_job_application_notification
from.models import *
from company.models import Job_Application,Job_Vacancy,Company,Notification,Skills
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.utils import timezone
from custom_admin.models import User
from django.http import HttpResponse, Http404
from django.db.models import Q
from company.models import Job_Application
from .forms import JobApplicationForm

# Create your views here.

@login_required(login_url='signin')
def home(request):
    search = request.GET.get('search')
    location = request.GET.get('location')
    page_number = request.GET.get('page',1)
    company = Company.objects.all()
    jobs = Job_Vacancy.objects.all().order_by('-posted')

    employee = request.user.employee
    job_applications = Job_Application.objects.filter(employee=employee)
    notify = Notification.objects.filter(employee=employee)
    notifications =[] 
    for i in job_applications:
        if i.status != 'submitted':
            notification = f" {i.job_vacancy} you have applied {i.status} by {i.job_vacancy.company} "
            notifications.append(notification)
    count =len(notifications)        
    
    if search:
        jobs = jobs.filter(designation__icontains=search)

    if location:
        jobs = jobs.filter(location__icontains = location )

    job_application = Job_Application.objects.filter(employee = request.user.employee)
    li=[]
    for i in job_application:
       
        li.append(i.job_vacancy.id)
    # count = len(li)


    paginator = Paginator(jobs,3)
    page = paginator.page(page_number)
    jobs = page.object_list
    
    context={
        
        'jobs':jobs,
        'company':company,
        'job_application':job_application,
        'li':li,
        'notifications':notifications,
        'count':count,
        'pages':list(range(1,paginator.num_pages+1))
    }
    
    return render(request,'employee_account/home.html',context)


def job_listing(request):
    print(f'\n\n\n{request.GET}\n\n\n')
    employee = request.user.employee
    search = request.GET.get('search')
    location = request.GET.get('location')
    page_number = request.GET.get('page',1)
    company = Company.objects.all()
    jobs = Job_Vacancy.objects.all().order_by('-posted')
    job_type = request.GET.get('job_type')
    search_by_date = request.GET.get('search_by_date')
    experience_from = request.GET.get('experience_from',None)
    experience_to = request.GET.get('experience_to',None)
    date_filter = Q()

    
    employee_skills = set(SkillSet.objects.filter(profile__user=employee).values_list('skill',flat=True))
    recommended_jobs = []
    print(employee_skills)
    for job_vacancy in jobs:
        job_vacancy_skills = set(Skills.objects.filter(job_vacancy =job_vacancy).values_list('skill_name',flat=True))
        print(job_vacancy_skills)
        if employee_skills.issubset(job_vacancy_skills):
            recommended_jobs.append(job_vacancy)
     
    no_of_recommended = len(recommended_jobs)        
    print(recommended_jobs)
    if job_type:
        jobs = jobs.filter(job_type__icontains = job_type)

    if search_by_date:
        if search_by_date == 'today':
            date_filter = Q(posted__date=timezone.now().date())
        elif search_by_date == 'last 2 days':
            date_filter = Q(posted__date__gte=timezone.now().date()-timedelta(days=2))
        elif search_by_date == 'last 3 days':
            date_filter = Q(posted__date__gte=timezone.now().date()-timedelta(days=3))
        elif search_by_date == 'last 5 days':
            date_filter = Q(posted__date__gte=timezone.now().date()-timedelta(days=5))
        elif search_by_date == 'last 10 days':
            date_filter = Q(posted__date__gte=timezone.now().date()-timedelta(days=10))

        jobs = jobs.filter(date_filter)
    
    
    if request.method == 'POST':
        salary_from = request.POST.get('salary_from')
        salary_to = request.POST.get('salary_to')
        if salary_from and salary_to:
            jobs = jobs.filter(salary_from__gte=salary_from, salary_to__lte=salary_to)
        else:
            jobs = Job_Vacancy.objects.all()
    
    if search:
        jobs = jobs.filter(designation__icontains=search)

    if location:
        jobs = jobs.filter(location__icontains = location )


    job_application = Job_Application.objects.filter(employee = request.user.employee)
    li=[]
    for i in job_application:
       
        li.append(i.job_vacancy.id)
    count = len(li)

    paginator = Paginator(jobs,6)
    page = paginator.page(page_number)
    jobs = page.object_list
    
    context={
        'recommended_jobs':recommended_jobs,
        'recommended':no_of_recommended,
        'jobs':jobs,
        'company':company,
        'job_application':job_application,
        'li':li,
        'count':count,
        'pages':list(range(1,paginator.num_pages+1))
    }
    
    return render(request,'employee_account/job_listing.html',context)




def job_details(request,id):
    job = Job_Vacancy.objects.get(id = id)
    company_id = job.company
    company_profile = Job_Vacancy.objects.filter(company=company_id)
    job_application = Job_Application.objects.filter(employee = request.user.employee)
    li=[]
    for i in job_application:
       
        li.append(i.job_vacancy.id)
    context={
        'company_id':company_id, 
        'company':company_profile,
        'job':job,
        'job_application':job_application,
        'li':li,
        'skills':job.skills_set.all()
    }
    return render(request,'employee_account/job_details.html',context)

def company_details(request,id):
    company = Company.objects.get(id=id)
    
    context={
        'company':company,
    }
    return render(request,'company/profile.html',context)



def register(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dob = request.POST.get('dob')
        # dob = datetime.strptime(dob, '%Y-%m-%d').date()
        profile_img = request.FILES.get('p_image')
        resume = request.FILES.get('resume')
        password = request.POST.get('password')
        re_password = request.POST.get('password2')

        if password == re_password:
            user = User.objects.filter(email=email).first()
            if not user:
                user = User.objects.create_user(
                    first_name=f_name,
                    last_name=l_name,
                    username=username,
                    email=email,
                    password=password,
                    is_employee=True
                )
                Employee.objects.create(
                    user=user,
                    DOB=dob,
                    profile_img=profile_img,
                    email=email,
                    phone=phone,
                    resume=resume
                )
                ProfileDetails.objects.create(
                    user = user.employee,
                    profile_img = profile_img,
                   
                )
                messages.success(request, 'Account created successfully')
                return redirect('signin')
            else:
                messages.error(request, 'Account already exists')
        else:
            messages.error(request, 'Invalid password or credentials')

    return render(request,'employee_account/registeration.html')



@login_required(login_url='signin')
def employee_profile(request):
    if request.user.is_authenticated:
        try:
            employee = Employee.objects.get(user=request.user)
            profile = ProfileDetails.objects.filter(user=request.user.employee).first()
            context ={
                'employee':employee,
                'profile':profile,
                'skills': profile.skillset_set.all()
            }
            return render(request,'employee_account/emp_profile.html',context)
        except Employee.DoesNotExist:
            raise Http404('profile not exist')
    else:
        raise Http404('You are not authorized to this page')

@login_required(login_url='signin')
def view_resume(request, profile_id):
    profile = get_object_or_404(ProfileDetails, pk=profile_id)
    context = {'profile': profile}
    return render(request, 'employee_account/resume_view.html', context)

# def sign_in(request):
#     if request.method == 'POST':
#         username = request.POST.get('email')
#         password = request.POST.get('password')
#         user = authenticate(username = username,password=password)
#         if user is not None:
#             login(request,user)
#             return redirect('home')
#         else:
#             messages.error(request,'no account found')
#         messages.error(request,'invalid credentials')   
#     return render(request,'employee_account/signin.html')


def sign_out(request):
    logout(request)
    return redirect('signin')


@login_required(login_url='signin')
def job_application_create(request,id):
    job_vacancy=Job_Vacancy.objects.get(id=id)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            job_application = form.save(commit=False)
            job_application.employee = request.user.employee 
            job_application.job_vacancy = job_vacancy
            job_application.company = job_vacancy.company
            job_application.save()
            # create_job_application_notification.send(sender=Job_Application, instance=job_application, created=True, request=request)

            messages.success(request, 'Job application submitted successfully.')
            return redirect('job_application_detail')
        
    else:
        form = JobApplicationForm()
    context = {
        "job_vacany":job_vacancy,
        "form":form,
        "request":request
    }    
    
    return render(request, 'employee_account/job_application_create.html', context)




@login_required(login_url='signin')
def job_application_detail(request):
    #job_application = get_object_or_404(Job_Application, id=id)
    job_application  = Job_Application.objects.filter(employee = request.user.employee).order_by('-applied')
    
    
    return render(request, 'employee_account/job_application_details.html', {'job_application': job_application})

@login_required(login_url='signin')
def employee_profile_edit(request):
    employee = request.user.employee
    profile = employee.profile.first()


    if request.method == 'POST':
        profile_img = request.FILES.get('edit_image')
        about = request.POST.get('about')
        experience = request.POST.get('experience')
        skills = request.POST.get('skills')
        education = request.POST.get('education')
        hobbies = request.POST.get('hobbies')
        
        
        employee.profile_img = profile_img
        employee.save()

        if not profile:
            profile = ProfileDetails(user=employee)
        
        profile.profile_img = profile_img
        profile.about = about
        profile.experience = experience
        profile.skills = skills
        profile.education = education
        profile.hobbies = hobbies
    
        profile.save()
        messages.success(request,'saved changes')
    
    

    context = {
        'profile': profile,
    }

    return render(request, 'employee_account/employee_profile_edit.html', context)



#Experience Edit
@login_required(login_url='signin')
def experience_edit(request,id):
    experience = Experience.objects.get(id = id)
    
    if request.method == 'POST':
        experience.position = request.POST.get('position')
        experience.company = request.POST.get('company')
        experience.location = request.POST.get('location')
        experience.year_started = request.POST.get('year_started')
        experience.year_ended = request.POST.get('year_ended')
        experience.description = request.POST.get('description')
        experience.save()
        return redirect('employee_profile')
    context = {
        'experience':experience
    }
    print(experience)
    return render(request,'employee_account/emp_profile.html',context)


@login_required(login_url='signin')
def add_skill(request):
    print(request.user.employee)
    if request.method == 'POST':
        skill_name = request.POST.get('skillName')
        profile = ProfileDetails.objects.get(user = request.user.employee)
        
        if profile:
            SkillSet.objects.create(profile=profile, skill=skill_name)
        
        return redirect('employee_profile')  

    return render(request, 'employee_account/emp_profile.html')



@login_required(login_url='signin')
def add_experience(request):
    if request.method == 'POST':
        position = request.POST.get('position')
        company  = request.POST.get('company')
        location = request.POST.get('location')
        year_started = request.POST.get('year_started')
        year_ended  = request.POST.get('year_ended')
        description = request.POST.get('description')
        profile = ProfileDetails.objects.get(user = request.user.employee)

        if profile:
            Experience.objects.create(
                profile = profile,
                position = position,
                company = company,
                location = location,
                year_started = year_started,
                year_ended = year_ended,
                description = description
            )
        return redirect('employee_profile')
    return render(request,'employee_account/emp_profile.html')


@login_required(login_url='signin')
def add_education(request):
    if request.method == 'POST':
        university = request.POST.get('university')
        year_started = request.POST.get('year_started')
        year_ended = request.POST.get('year_ended')
        course = request.POST.get('course')
        profile = ProfileDetails.objects.get(user = request.user.employee)

        if profile:
            Education.objects.create(
                profile =profile,
                university_college = university,
                year_started = year_started,
                year_ended = year_ended,
                course = course
            )
            return redirect('employee_profile')
        return render(request,'employee_account/emp_profile.html')
    


@login_required(login_url='signin')
def add_project(request):
    if request.method == 'POST':
        project_name = request.POST.get('project_name')
        project_file = request.FILES.get('project_file')
        description = request.POST.get('description')
        profile = ProfileDetails.objects.get(user = request.user.employee)

        if profile:
            Project.objects.create(
                project_name = project_name,
                project_file = project_file,
                description  = description,
                profile = profile
            )
            return redirect('employee_profile')
        return render(request,'employee_account/emp_profile.html')



#jobs-status-notification
@login_required(login_url='signin')
def my_jobs(request):
    print(notification)
    employee = request.user.employee
    job_applications = Job_Application.objects.filter(employee=employee)
    notify = Notification.objects.filter(employee=employee)
    notifications =[]
    for i in job_applications:
        if i.status != 'submitted':
            notification = f"{i.job_vacancy} you have applied {i.status} by {i.job_vacancy.company} "
            notifications.append(notification)        
    context = {
        'job_applications': job_applications,
        'notifications': notifications,
       
                
    }
    return render(request, 'employee_account/base.html', context)



@login_required(login_url='signin')
def password_reset(request):
    user = request.user.employee
    profile = user.user
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            profile.set_password(password2)
            profile.save()
            messages.success(request,'password changed')
            return redirect('employee_profile')
        messages.success(request,'password doesn not match')
        return redirect('password_reset')
    return render(request,'employee_account/password_reset.html')

