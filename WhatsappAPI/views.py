from django.http import HttpResponse
from django.shortcuts import render
from twilio.rest import Client
from django.views.decorators.csrf import csrf_exempt
account_sid = 'ACff1c255543fb69ccf7c78b54ee85d2ee'
auth_token = '25d3bc402171e7e2840bdee6d6091237'
client = Client(account_sid, auth_token)

# Create your views here.
@csrf_exempt
def bot(request):
    # print(request.POST)
    # message = request.POST['Body']
    # sender_name = request.POST['ProfileName']
    # sender_number = request.POST['From']
    # print(message, sender_name, sender_number)
    if request.method == 'POST':
        if 'Body' in request.POST:
            message = request.POST['Body']
            # rest of your code
        else:
            print("Body not in POST data")
    return HttpResponse("hello")

@csrf_exempt
def reply(request):
    message = client.messages.create(
        from_ = 'whatsapp:+14155238886',
        body = "hey there, How are you?",
        to = 'whatsapp:+917058921518',

        )
    
    print(message.sid)
