from django.urls import path
from requests import request
from . import views
urlpatterns = [
    path('', views.messages_page,name='messages-page'),
    path('chat_id/<str:pk>/',views.chat_id,name='chat_id'),
    
]
