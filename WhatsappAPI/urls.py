from django.urls import path
from .views import bot
from .Views2 import whatsapp_webhook, process_message
from .views11M import whatsapp_webhook, send_first_message


urlpatterns = [
    path('whatsapp/webhook/', whatsapp_webhook, name='whatsapp_webhook'),
    # Add other URL patterns as needed for specific actions based on processed message
    path('whatsapp/action/', process_message, name='process_message'),


    path('webhook',view = whatsapp_webhook, name='whatsapp_webhook'),
    path('api/send_first_message/', view = send_first_message, name = "sfm"),
]
