from django.urls import path
from .views import bot

from .view11M import whatsapp_webhook, send_first_message


urlpatterns = [

    path('webhook',view = whatsapp_webhook, name='whatsapp_webhook'),
    path('api/send_first_message/', view = send_first_message, name = "sfm"),
]
