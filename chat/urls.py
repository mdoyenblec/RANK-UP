from django.urls import path
from . import views

urlpatterns = [
    path('chats/', views.chat_list_view, name='chat_list'),
    path('chats/<str:username>/', views.chat_list_view, name='chat_list'),
]
