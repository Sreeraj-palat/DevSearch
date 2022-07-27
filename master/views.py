from users.forms import ProfileForm
from users.models import Profile
from multiprocessing import context
from unicodedata import name
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group 
from django.contrib import messages
from users.decorators import allowed_users
from django.views.decorators.csrf import csrf_exempt
from payments.models import Payments
from recruter.models import Job
from projects.models import Project
from django.db.models import Sum


# Create your views here.
@csrf_exempt
def masterLogin(request):

    page = 'master-login'
    if request.user.is_authenticated:
        return redirect('master-home')

    if request.method == 'POST':
        request.session['admin'] = 'admin'
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)

        except:
            messages.error(request,'username doesnot exist')

        user = authenticate(request, username=username, password=password)

        if user.is_superuser:
            if user is not None:
                login(request,user)
                return redirect('master-home')
            else:
                messages.error(request,'username or password is incorrect') 

        else:
            messages.error(request, 'unauthenticated entry..')    

    group = Group.objects.all()                  
    context = {'page':page, 'group':group}
    return render(request,'master/master_login.html', context)

def masterLogout(request):
    logout(request)
    messages.error(request,'user was succesfully logout')
    return redirect('master-login')     



# @allowed_users(allowed_role=['Master'])
@csrf_exempt
def masterHome(request):
    dev_group = Group.objects.get(name='Developer')
    dev_users = dev_group.user_set.all()
    print(dev_users)

    rec_group = Group.objects.get(name='Recruter')
    rec_users = rec_group.user_set.all()

    user_count = User.objects.count()
    project_count = Project.objects.count()
    job_count = Job.objects.count()
    
    # payment_sum = Payments.objects.all().aggregate(sum('amount_rs'))
    
    context = {
        'dev_users':dev_users, 
        'dev_group':dev_group,
        'rec_group':rec_group,
        'rec_users':rec_users,
        'user_count':user_count,
        'project_count':project_count,
        # 'payment_sum':payment_sum,
        'job_count':job_count
        }
    return render(request,'master/master_home.html', context)    


# @allowed_users(allowed_role=['Master'])
def paymentList(request):
    payment = Payments.objects.all()
    print(payment) 

   
   
    
    context = {'payment':payment,}
    return render(request,'master/payment_list.html', context)   



# @allowed_users(allowed_role=['Master'])
def paymentDetails(request,pk,id):  
    pay_id = Payments.objects.get(id=id)
    print(pay_id)
    amount = int(pay_id.amount)/100
    print(amount)
    balence = float(amount)-float(pay_id.dev_commission)
    print(balence)
    profile = Profile.objects.get(id=pk)

    context = { 'profile':profile, 'pay_id':pay_id,'amount':amount, 'balence':balence}
    return render(request,'master/payment_details.html', context)  

# @allowed_users(allowed_role=['Master'])
def updatePayment(request,pk):
    pay_id = Payments.objects.get(id=pk)
    if pay_id.paid_to_dev == False:
        pay_id.paid_to_dev = True
        messages.success(request,'Payment updated successfully')
    pay_id.save() 
   
    return redirect('payment-list')      


# @allowed_users(allowed_role=['Master'])
def jobList(request):
    job = Job.objects.all()
    context = {'job':job}
    return render(request,'master/job_list.html', context) 


# @allowed_users(allowed_role=['Master'])
def projectList(request):
    project = Project.objects.all()
    context = {'project':project}
    return render(request,'master/project_list.html', context)   


# @allowed_users(allowed_role=['Master'])
def usersList(request):
    users = User.objects.all()
    context = {'users':users}
    print(users)
    return render(request,'master/user_list.html', context)      


# @allowed_users(allowed_role=['Master'])
def editUser(request,pk):
    user = User.objects.get(id=pk)
    context = {'user':user}
    if request.method == "POST":
        user.username = request.POST['username']
        user.name = request.POST['first_name']
        user.email = request.POST['email'] 
        
        user.save()

        messages.success(request,'Successfully Changed')
        return redirect('user-list')
    return render(request,'master/user_update_form.html',context)  


# @allowed_users(allowed_role=['Master'])
def blockUser(request, pk):
    user = User.objects.get(id=pk)
    if user.is_active:
        user.is_active = False
        messages.success(request, 'user is Blocked Successfully')
    else:
        user.is_active = True
        messages.success(request, 'user is un Blocked Successfully')

    user.save()
    return redirect('user-list')        
    
