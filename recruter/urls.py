from django.urls import path
from . import views


urlpatterns =[
    path('recruter/',views.recruter,name='recruter'),
    path('create-job/',views.createJob, name='create-job'),
    path('update-job/<str:pk>/',views.updateJob, name='update-job'),
    path('delete-job/<str:pk>/',views.deleteJob, name='delete-job'),
    path('job-details/<str:pk>/',views.jobDetails, name='job-details'),


] 