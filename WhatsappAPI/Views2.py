from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from django.http import HttpResponseNotAllowed

@csrf_exempt
def whatsapp_webhook(request):
    if request.method == 'POST':
        # Handle incoming message
        incoming_message = request.POST.get('Body', '')
        
        # Process the incoming message
        response_message = process_message(incoming_message)
        print(response_message)
        
        # Prepare TwiML response
        twiml_response = MessagingResponse()
        twiml_response.message(response_message)
        
        return HttpResponse(str(twiml_response))
    else:
        return HttpResponseNotAllowed(['POST'])


def process_message(message):
    # Add your custom logic to process the incoming message
    # For example, you can analyze the message and generate a response accordingly
    # Here's a simple example
    if message.lower() == 'hello':
        return "Hi there! How can I assist you?"
    else:
        return "I'm sorry, I didn't understand that. Please try again."
