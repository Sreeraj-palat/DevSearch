from django.db import models
from django.db import models
import uuid
from users.models import Profile

# Create your models here.

class Job(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    featured_image = models.ImageField(null=True,blank=True, default="default.jpg")
    created = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.title 