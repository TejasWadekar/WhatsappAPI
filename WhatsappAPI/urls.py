from django.urls import path
from .views import bot
from .views12 import whatsapp_webhook, send_first_message

urlpatterns = [
    path('webhook', whatsapp_webhook, name='whatsapp_webhook'),
    path('api/send_first_message/', send_first_message, name="sfm"),
]
