from multiprocessing import context
from django.shortcuts import render, redirect

from users.views import response
from .models import Payments
from .forms import PaymentForm
from users.models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from django.views.decorators.csrf import csrf_exempt
import razorpay






# Create your views here.
@login_required(login_url='login')
@csrf_exempt
def Payment(request,pk):
    recipient = Profile.objects.get(id=pk)
    if request.method == "POST":
        
        sender = request.user.profile
        print(sender)
        name = request.POST.get('name')
        amount = int(request.POST.get('amount'))*100
        amount_rs = request.POST.get('amount')
        payment_note = request.POST.get('payment_note')
        dev_commission = (amount/100)*15/100

        # create Razorpay client
        client = razorpay.Client(auth=('rzp_test_7faFV5PWWZYXeb', 'PEmHIBuXxsbYfIU6XxgaiqXl'))

        # create order
        response_payment = client.order.create(dict(amount=amount,
                                                    currency='INR')
                                               )

        order_id = response_payment['id']
        order_status = response_payment['status']

        if order_status == 'created':
            payment = Payments(
                name=name,
                amount=amount,
                order_id=order_id,
                payment_note = payment_note,
                recipient = recipient,
                sender = sender,
                dev_commission = dev_commission,
                amount_rs=amount_rs

            )
            payment.save()
            response_payment['name'] = name

            form = PaymentForm(request.POST or None)
            return render(request, 'payments/payment_form.html', {'form': form, 'payment': response_payment})

    form = PaymentForm()
    return render(request, 'payments/payment_form.html', {'form': form, 'recipient':recipient})



@login_required(login_url='login')
@csrf_exempt
def PaymentStatus(request):
    response = request.POST
    params_dict = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature']
    }

    # client instance
    client = razorpay.Client(auth=('rzp_test_7faFV5PWWZYXeb', 'PEmHIBuXxsbYfIU6XxgaiqXl'))

    try:
        status = client.utility.verify_payment_signature(params_dict)
        payment = Payments.objects.get(order_id=response['razorpay_order_id'])
        payment.razorpay_payment_id = response['razorpay_payment_id']
        payment.paid = True
        payment.save()
        return render(request, 'payments/payment_status.html', {'status': True})
    except:
        return render(request, 'payments/payment_status.html', {'status': False})   


       