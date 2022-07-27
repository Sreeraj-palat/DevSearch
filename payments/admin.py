from django.contrib import admin
from .models import Payments

# Register your models here.

class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('sender','recipient','name','amount','payment_note','order_id','razorpay_payment_id','paid',)
    ordering = ('-created',)

admin.site.register(Payments,PaymentsAdmin)
