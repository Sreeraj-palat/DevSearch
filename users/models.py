from django.db import models
from django.contrib.auth.models import User, AbstractUser
import uuid


from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings




# Create your models here.


# class Roles(models.Model):
#     name = models.CharField(max_length=200)
#     created = models.DateTimeField(auto_now_add=True)
#     id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True,editable=False)
 
#     def __str__(self):
#         return self.name 
# class User(AbstractUser):
#     is_dev = models.BooleanField(default=False)
#     is_rec = models.BooleanField(default=False)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    short_intro = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profiles/',default="profiles/user-default.png")
    social_github = models.CharField(max_length=200, blank=True, null=True)
    social_twitter = models.CharField(max_length=200, blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    social_youtube = models.CharField(max_length=200, blank=True, null=True)
    social_website = models.CharField(max_length=200, blank=True, null=True)
    is_dev = models.BooleanField(default=False)
    is_rec = models.BooleanField(default=False)
    phone = models.CharField(max_length=11,null=True,blank=True)
    bank_name = models.CharField(max_length=200, blank=True, null=True)
    bank_branch = models.CharField(max_length=200, blank=True, null=True)
    ifsc = models.CharField(max_length=11,blank=True, null=True)
    account_number = models.CharField(max_length=16,blank=True, null=True)
    beneficiary_name = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.user.username)

    @property
    def imageURL(self):
        try:
            url = self.profile_image.url
        except:
            url = ''
        return url      
        
                          

class Skill(models.Model):
    owner =  models.ForeignKey(Profile, on_delete=models.CASCADE, null=True,blank=True)
    name = models.CharField(max_length=200, blank=True, null=True) 
    description = models.TextField(blank=True, null=True)
   

    def __str__(self):
        return str(self.name)




class Message(models.Model):
    sender = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True, blank=True)
    recipient = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True,blank=True, related_name="messages")
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
   
 

def __str__(self):
    return self.subject


class Meta:
    ordering = ['is_read','-created']    
     

