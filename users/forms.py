
from cProfile import label
from dataclasses import field
import imp
from operator import mod
from pyexpat import model
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Skill, Message


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name':'Name',
        }

    def __init__(self,*args, **kwargs):
        super(CustomUserCreationForm,self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})     


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name','email', 'username', 'location','bio','short_intro','profile_image','social_github','social_linkedin','social_twitter','social_website','phone','bank_name','bank_branch','ifsc','account_number','beneficiary_name']
        labels = {
            'social_github':'Github',
            'social_linkedin':'Linkedin',
            'social_twitter':'Twitter',
            'social_website':'Personal Website',

        }
    def __init__(self,*args, **kwargs):
        super(ProfileForm,self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})    



class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = ['name','description']
        labels = {
            'name':'Skill Name',
        }
        
        

    def __init__(self,*args, **kwargs):
        super(SkillForm,self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})     


class ResponseForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name','email','subject','body']  
        labels = {
            'body' : 'Describe Yourself'
        } 

    def __init__(self,*args, **kwargs):
        super(ResponseForm,self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})         