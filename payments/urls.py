from django.urls import path
from . import views

urlpatterns = [
    path('payment-form/<str:pk>',views.Payment,name='payment-form'),
    path('payment-status/',views.PaymentStatus,name='payment-status'),
    

]