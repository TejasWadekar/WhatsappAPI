from django.http import HttpResponse
from django.shortcuts import render
from twilio.rest import Client
from django.views.decorators.csrf import csrf_exempt
account_sid = 'ACff1c255543fb69ccf7c78b54ee85d2ee'
auth_token = '44dec42d16c77d02eef9344aa803f0e7'
client = Client(account_sid, auth_token)

# Create your views here.
@csrf_exempt
def bot(request):
    print(request.POST)
    # message = request.POST['Body']
    # sender_name = request.POST['ProfileName']
    # sender_number = request.POST['From']
    # if message == "hi":
    #     client.messages.create(
    #         from_ = 'whatsapp:+14155238886',
    #         body = f"hi {sender_name} How are you?",
    #         to = 'whatsapp:+917058921518',

    #     )
    return HttpResponse("hello")
