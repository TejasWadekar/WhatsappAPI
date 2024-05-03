# views.py

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from django.conf import settings
from twilio.rest import Client

# Initialize Twilio Client with your Account SID and Auth Token
account_sid = 'ACff1c255543fb69ccf7c78b54ee85d2ee'
auth_token = '25d3bc402171e7e2840bdee6d6091237'
client = Client(account_sid, auth_token)

# List of questions to ask the candidate
questions = [
    "What is your name?",
    "What is your email address?",
    "What is your phone number?",
    # Add more questions here as needed
]

# Initialize conversation state
conversation_state = {
    'current_question_index': 0,
    'answers': {}
}

@csrf_exempt
def whatsapp_webhook(request):
    if request.method == 'POST':
        # Get the incoming message data
        body = request.POST.get('Body', '')
        sender = request.POST.get('From', '')

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
