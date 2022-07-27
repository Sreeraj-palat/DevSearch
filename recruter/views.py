from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from recruter.models import Job
from . forms import jobForm
from users.models import Profile


# Create your views here.

def recruter(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    jobs = Job.objects.distinct().filter(
        Q(title__icontains=search_query)|
        Q(owner__name__icontains=search_query)
    )
    context = {'jobs':jobs, 'search_query':search_query}
    return render(request,'recruter/recruter.html', context)


@login_required(login_url='login')
def createJob(request):
    profile = request.user.profile
    form = jobForm()

    if request.method == 'POST':
        form = jobForm(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')

    context = {'form' : form}
    return render(request, 'recruter/job_form.html',context)




def jobDetails(request, pk):
    jobObj = Job.objects.get(id=pk)
    
    return render(request, 'recruter/job_details.html',{'job':jobObj})




@login_required(login_url='login')
def updateJob(request, pk):
    profile = request.user.profile
    job = profile.job_set.get(id=pk)
    form = jobForm(instance=job) 
    if request.method == 'POST':
        form = jobForm(request.POST,request.FILES, instance=job)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form' : form}
    return render(request, 'recruter/job_form.html',context) 




@login_required(login_url='login')
def deleteJob(request, pk):
    profile = request.user.profile
    job = profile.job_set.get(id=pk)
    if request.method == 'POST':
        job.delete()
        return redirect('account')
    context = {'object': job}
    return render(request,'delete_template.html', context)