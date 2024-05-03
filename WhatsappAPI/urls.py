from django.urls import path
from .views import bot
from .Views2 import whatsapp_webhook, process_message
from .views3 import whatsapp_webhook


urlpatterns = [
    path('',view=bot),
    path('whatsapp/webhook/', whatsapp_webhook, name='whatsapp_webhook'),
    # Add other URL patterns as needed for specific actions based on processed message
    path('whatsapp/action/', process_message, name='process_message'),
    path('reply/', reply, name='reply'),

    path('webhook',view = whatsapp_webhook, name='whatsapp_webhook'),
]
