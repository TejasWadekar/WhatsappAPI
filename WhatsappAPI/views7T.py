from googletrans import Translator
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
auth_token = '25d3bc402171e7e2840bdee6d6091237'
client = Client(account_sid, auth_token)

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
    'answers': {},
    'conversation_ended': False #Added this new line if bot is asking again 
}

# Initialize translator
translator = Translator()

def translate_text(text, dest_language):
    # Translate the text to the destination language
    translation = translator.translate(text, dest=dest_language)
    return translation.text

@api_view(['POST'])
def send_first_message(request):
    global conversation_state

    # Resetting conversation state for new chat
    conversation_state['current_question_index'] = 0
    conversation_state['answers'] = {}
    conversation_state['conversation_ended'] = False  # Reset the flag here

    name = request.data.get('name')
    hrname = request.data.get('hrname')
    phoneNo = request.data.get('phoneNo')

    # Actual First Message Transfer
    message_body = f"Dear {name},\n\nI hope this message finds you well. My name is {hrname} and I am reaching out to you regarding your recent application with us.\n\nIn order to proceed with the next steps in our hiring process, we require some additional information from you. We have a few questions that will help us better understand your fitment for the role.\n\nYour prompt response will be greatly appreciated and will enable us to move forward with your application.\nThank you for your time and cooperation.\n\nBest regards, {hrname}\n\n Please Type Start. "
    translated_message_body = translate_text(message_body, 'es')  # Translate to Spanish
    message = client.messages.create(body=translated_message_body, from_='whatsapp:+14155238886', to=phoneNo)
  
    print(message.sid)

def process_message(message, sender):
    global conversation_state

    # If the conversation has ended, Needs to stop
    if conversation_state['conversation_ended']:
        return "Thank you for your time. Have a great day!" 
    # Get current question index
    current_question_index = conversation_state['current_question_index']

    # Store the answer to the current question
    conversation_state['answers'][current_question_index] = message

    # Check if there are more questions
    if current_question_index < len(questions) - 1:
        # Move to the next question
        conversation_state['current_question_index'] += 1
        next_question = questions[current_question_index + 1]
        translated_next_question = translate_text(next_question, 'es')  # Translate to Spanish
        return translated_next_question
    else:
        # End of conversation, generate summary
        summary = generate_summary()
        translated_summary = translate_text(summary, 'es')  # Translate to Spanish
        return translated_summary

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
    conversation_state['conversation_ended'] = True

    return summary
