from django.urls import path
from . import views
from django.shortcuts import render
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.chat_home, name='chat_home'),
    path('process_query/', views.process_query, name='process_query'),
    path('fetch_chat_history/', views.fetch_chat_history, name='fetch_chat_history'),
    path('view/<uuid:chat_id>/', views.view_chat, name='view_chat'),
    path('extract_text_from_url/', views.extract_text_from_url, name='extract_text_from_url'),
    path('extract_text_from_file/', views.extract_text_from_file, name='extract_text_from_file'),
    path('transcribe_audio/', views.transcribe_audio, name='transcribe_audio'),
    path('set_paragraph_context/', views.set_paragraph_context, name='set_paragraph_context'),
    
    
]
