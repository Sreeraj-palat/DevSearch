
from unicodedata import name
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from payments.models import Payments
from . models import Profile, Skill, Message
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group 
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import CustomUserCreationForm, ProfileForm,SkillForm, ResponseForm
from .decorators import allowed_users
from recruter.models import Job
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def whoLogin(request):
    context = {}
    return render(request,'users/confirm.html')

@csrf_exempt
def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)

        except:
            messages.error(request,'username doesnot exist')

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request,user)
            request.session['username'] = username
            return redirect(request.GET['next']if 'next' in request.GET else 'account')
        else:
            messages.error(request,'username or password is incorrect')            

    return render(request,'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.error(request,'user was succesfully logout')
    return redirect('login') 

@csrf_exempt
def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            group = Group.objects.get(name='Developer')
            user.groups.add(group)
            messages.success(request, 'User account was created')
            login(request, user)
            return redirect('edit-account')

        else:
            messages.success(request,'An error occurred during registration')    

    context = {'page':page, 'form':form}
    return render(request,'users/login_register.html',context)

@csrf_exempt
def recuterRegister(request):
    page = 'rec-register'
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            group = Group.objects.get(name='Recruter')
            user.groups.add(group)
            messages.success(request, 'User account was created')
            login(request, user)
            return redirect('edit-account')

        else:
            messages.success(request,'An error occurred during registration')    

    context = {'page':page, 'form':form,}
    return render(request,'users/login_register.html',context)
        
       

def profiles(request):
        search_query = ''
        if request.GET.get('search_query'):
            search_query = request.GET.get('search_query')
        skills = Skill.objects.filter(name__icontains=search_query)    
        
        profiles = Profile.objects.distinct().filter(
        Q (name__icontains=search_query)|
        Q(short_intro__icontains=search_query)|
        Q(skill__in=skills)
            )
        context = {'profiles':profiles, 'search_query': search_query}
        return render (request, 'users/profiles.html', context)


def userProfile(request,pk):
    profile = Profile.objects.get(id=pk)
    group = Group.objects.get(name='Developer')
    user = User.objects.all()

    topskills = profile.skill_set.exclude(description__exact="")
    otherskills = profile.skill_set.filter(description="")

    context = {'profile' : profile, 'topskills':topskills, 'otherskills':otherskills, 'group':group, 'user':user}
    return render(request, 'users/user-profile.html', context)    


        


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile

    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    jobs = profile.job_set.all()

    group = Group.objects.all()
    user = User.objects.all()
    
    context = {'profile' : profile, 'skills':skills, 'projects':projects, 'group':group, 'user':user, 'jobs':jobs}
    return render(request,'users/account.html', context)    


@login_required(login_url='login')
@csrf_exempt
def editAccount(request):
    profile = request.user.profile
    user = request.user
    form = ProfileForm(instance=profile)
    group = Group.objects.get(name='Developer')
    users = User.objects.filter(groups = group)
    print(users)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            if user in users:
                profile.is_dev = True
            else:
                profile.is_rec = True    
            form.save()
            return redirect('account')


    context = {'form':form}
    return render(request, 'users/profile_form.html',context)
 



@login_required(login_url='login')
@csrf_exempt
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request,'New Skill Added') 
            return redirect('account')

    context = {'form':form}
    return render(request,'users/skill_form.html', context)  




@login_required(login_url='login')
@csrf_exempt
def updateSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request,'Skill Updated') 
            return redirect('account')

    context = {'form':form}
    return render(request,'users/skill_form.html', context)  



@login_required(login_url='login')
@csrf_exempt
def deleteSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request,'Skill Deleted Succefully')
        return redirect('account')

    context = {'object': skill}
    return render(request,'delete_template.html', context)


@login_required(login_url='login')
def response(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()

    context = {'messageRequests':messageRequests, 'unreadCount':unreadCount}
    return render(request,'users/response.html', context)



     
@login_required(login_url='login')
def viewmessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message':message}
    return render(request, 'users/message.html', context)  


@login_required(login_url='login')
@csrf_exempt
def createResponse(request, id):
    
    recipient = Profile.objects.get(id=id)
    form = ResponseForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
                message.save()
            messages.success(request, 'Your Message was Successfully sent !')
            return redirect('create-response', id=recipient.id)

    context = {'recipient':recipient, 'form':form}
    return render(request, 'users/response_form.html', context)  


@login_required(login_url='login')
def wallet(request):
    profile = request.user.profile
    print(profile)
    payments= Payments.objects.all()
    pay = profile.recipient_dev.all()
    print(payments)
    context = {'pay':pay}
    return render(request,'users/wallet.html',context)


#context processor function
# def checkgroup(request):
#    user = request.user
#    print(user)
#    checkGroups = Group.objects.get(name='Recruter')
#    print(checkGroups)
#    persons = User.objects.filter(groups = checkGroups)
#    print(persons)
  
#    return {'persons':persons}



