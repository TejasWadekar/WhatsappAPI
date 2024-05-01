from django.http import HttpResponse
from django.shortcuts import render
from twilio.rest import Client
from django.views.decorators.csrf import csrf_exempt
account_sid = 'ACff1c255543fb69ccf7c78b54ee85d2ee'
auth_token = 'b4d00d19255f887be8e45852b2ddbfec'
client = Client(account_sid, auth_token)

# Create your views here.
@csrf_exempt
def bot(request):
    # print(request.POST)
    # message = request.POST['Body']
    # sender_name = request.POST['ProfileName']
    # sender_number = request.POST['From']
    # print(message, sender_name, sender_number)
    
    # client.messages.create(
    #     from_ = 'whatsapp:+14155238886',
    #     body = "How are you?",
    #     to = 'whatsapp:+917058921518',

    # )
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body='hello',
        to='whatsapp:+917058921518'
    )

    print(message.sid)
    # return HttpResponse("hello")
