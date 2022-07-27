import imp
from django.urls import path
from . import views

urlpatterns = [
    path('master-login/',views.masterLogin,name='master-login'),
    path('master-logout/',views.masterLogout,name='master-logout'),

    path('master-home/',views.masterHome,name='master-home'),

    path('payment-list',views.paymentList,name='payment-list'),
    path('payment-details/<str:pk>/<str:id>/',views.paymentDetails,name='payment-details'),
    path('update-payment/<str:pk>/',views.updatePayment,name='update-payment'),

    path('job-list',views.jobList,name='job-list'),

    path('project-list',views.projectList,name='project-list'),

    path('user-list',views.usersList,name='user-list'),
    path('edit-user/<str:pk>/',views.editUser,name='edit-user'),
    path('block-user/<str:pk>/',views.blockUser,name='block-user'),
]