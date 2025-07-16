from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('chat/', views.chat_view, name='chat'),
    path('chat-message/', views.chat_message, name='chat_message'),
    path('dance-chat/', views.chat_view, name='dance_chat'),
    path('dance-chat-message/', views.chat_message, name='dance_chat_message'),
]
