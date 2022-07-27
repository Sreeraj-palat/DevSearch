import imp
import uuid
from django.db import models
from users.models import Profile

# Create your models here.


class Payments(models.Model):
    sender = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True, blank=True)
    recipient = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True,blank=True,related_name="recipient_dev")
    name = models.CharField(max_length=200, null=True, blank=True)
    amount = models.CharField(max_length=200)
    amount_rs = models.CharField(max_length=200, null=True) 
    payment_note = models.CharField(max_length=500, null=True, blank=True)
    order_id = models.CharField(max_length=500,blank=True)
    razorpay_payment_id = models.CharField(max_length=500, blank=True)
    paid = models.BooleanField(default=False)
    dev_commission = models.IntegerField(default=0)
    paid_to_dev = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
 

def __str__(self):
    return self.amount


