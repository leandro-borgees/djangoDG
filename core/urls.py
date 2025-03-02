# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('webhook/<str:bot_token>/', views.telegram_webhook, name='telegram_webhook'),
]
