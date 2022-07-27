import profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from users.models import User, Profile

# Create your views here.
from chat.models import Thread



@login_required(login_url='login')
def messages_page(request):
    username = request.session['username']
    user = User.objects.get(username=username)
    print(user.id)
    profile = Profile.objects.all()
    threads = Thread.objects.by_user(user=user).prefetch_related('chatmessage_thread').order_by('timestamp')
    context = {
        'Threads': threads,
        'user':user,
        'profile':profile    
    }
    return render(request, 'chat/messages.html', context)

@login_required(login_url='login')
def chat_id(request,pk):
    username = request.session['username']
    user = User.objects.get(username=username)
    
    if Thread.objects.filter(first_person=user,second_person=pk).first():
        return redirect(messages_page)
    elif Thread.objects.filter(second_person=user,first_person=pk).first():
        return redirect(messages_page)

    else:
        
        first_person = User.objects.get(username=username)
        print(first_person)
        second_person = User.objects.get(pk=pk)
        thread = Thread.objects.create(
            first_person=first_person,
            second_person=second_person
            )
        thread.save()
        return redirect(messages_page)         


