import os
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

# Get your Twilio account_sid and auth_token from environment variables
account_sid = 'ACff1c255543fb69ccf7c78b54ee85d2ee'
auth_token = '25d3bc402171e7e2840bdee6d6091237'

@csrf_exempt
def bot(request):
    if request.method == 'POST':
        # Get the message the user sent our Twilio number
        body = request.POST.get('Body', '')

        # Start our TwiML response
        resp = MessagingResponse()

        # Determine the right reply for this message
        if 'hello' in body.lower():
            resp.message("Hi! How can I assist you today?")
        else:
            resp.message("Sorry, I didn't understand that. Could you please rephrase?")

        # Create a Twilio client
        client = Client(account_sid, auth_token)

        # Send a response message
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body="Hey there, How are you?",
            to='whatsapp:+917058921518'
        )

        print(message.sid)

        return HttpResponse(str(resp), content_type='text/xml')
    else:
        return HttpResponse("Request method must be POST.")
