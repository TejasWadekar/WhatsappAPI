import os
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

# Get your Twilio account_sid and auth_token from environment variables
account_sid = 'ACff1c255543fb69ccf7c78b54ee85d2ee'
auth_token = '25d3bc402171e7e2840bdee6d6091237'

client = Client(account_sid, auth_token)

@csrf_exempt
def bot(request):
    message = client.messages.create(body='Hello there!', from_='whatsapp:+14155238886', to='whatsapp:+917058921518')
  
    print(message.sid)
