from django.urls import path
from . import views

urlpatterns = [

    path('login/',views.loginUser, name='login'),
    path('logout/',views.logoutUser, name='logout'),
    path('register/',views.registerUser, name='register'),
    path('rec-register/',views.recuterRegister,name='rec-register'),
    path('who-login/',views.whoLogin, name='who-login'),

    path('',views.profiles, name='profiles'),
    path('profile/<str:pk>/',views.userProfile, name='user-profiles'),
    path('account/',views.userAccount,name='account'),
    path('edit-account/',views.editAccount, name='edit-account'),
    path('wallet/',views.wallet, name='wallet'),

    path('create-skill/',views.createSkill,name='create-skill'),
    path('update-skill/<str:pk>/',views.updateSkill,name='update-skill'),
    path('delete-skill/<str:pk>/',views.deleteSkill,name='delete-skill'),

    path('response/',views.response,name='response'),
    path('message/<str:pk>/',views.viewmessage,name='message'),
    path('create-response/<str:id>/',views.createResponse,name='create-response'),
   
]