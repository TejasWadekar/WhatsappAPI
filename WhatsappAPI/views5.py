# views.py

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from django.conf import settings
from twilio.rest import Client

# REST
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Initialize Twilio Client with your Account SID and Auth Token
account_sid = 'ACff1c255543fb69ccf7c78b54ee85d2ee'
auth_token = 'bf0e6597c58eda1602721e23a7e5566a'
client = Client(account_sid, auth_token)

# List of questions to ask the candidate
questions = [
    "Start ",
    "What is your current CTC?",
    "What is your expected CTC?",
    "What is your notice period (In days)?",
    "What is your current location?",
    "Are you willing to relocate?"
    # Add more questions here as needed
]

# Initialize conversation state
conversation_state = {
    'current_question_index': 0,
    'answers': {}
}

'whatsapp:+917058921518'

@api_view(['POST'])
def send_first_message(request):
    name = request.data.get('name')
    hrname = request.data.get('hrname')
    phoneNo = request.data.get('phoneNo')

    # Actual First Message Transfer
    message = client.messages.create(body=f"Dear {name},\n\nI hope this message finds you well. My name is {hrname} and I am reaching out to you regarding your recent application with us.\n\nIn order to proceed with the next steps in our hiring process, we require some additional information from you. We have a few questions that will help us better understand your fitment for the role.\n\nYour prompt response will be greatly appreciated and will enable us to move forward with your application.\nThank you for your time and cooperation.\n\nBest regards, {hrname}\n\n Please Type Start. ", from_='whatsapp:+14155238886', to=phoneNo)
  
    print(message.sid)

# For ending session try to use if method in whatsapp_webhook 'if send_first_message==True or POST' try for global in send_first make variable 
# False then only after phoneNo == sender from webhook set flag true

# This Conversation will get started when candidate replies to the first mesage sent by HR.
@csrf_exempt
def whatsapp_webhook(request):
    if request.method == 'POST':
        # Get the incoming message data
        body = request.POST.get('Body', '')
        sender = request.POST.get('From', '')
        print(request.POST)
        # Process the incoming message
        response = process_message(body, sender)

        # Create TwiML response
        twiml_response = MessagingResponse()
        twiml_response.message(response)

        return HttpResponse(str(twiml_response))
    else:
        return HttpResponse(status=405)  # Method not allowed

def process_message(message, sender):
    global conversation_state

    # Get current question index
    current_question_index = conversation_state['current_question_index']

    # Store the answer to the current question
    conversation_state['answers'][current_question_index] = message

    # Check if there are more questions
    if current_question_index < len(questions) - 1:
        # Move to the next question
        conversation_state['current_question_index'] += 1
        next_question = questions[current_question_index + 1]
        return next_question
    else:
        # End of conversation, generate summary
        summary = generate_summary()
        return summary

def generate_summary():
    global conversation_state
    answers = conversation_state['answers']

    # Construct summary from answers
    summary = "Thank you for your answers:\n"
    for i, question in enumerate(questions):
        summary += f"{question}\n- {answers.get(i, 'No answer provided')}\n"

    # Reset conversation state for next interaction
    conversation_state['current_question_index'] = 0
    conversation_state['answers'] = {}

    return summary
