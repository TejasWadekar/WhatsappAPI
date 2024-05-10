import requests, uuid, json
from langdetect import detect

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
auth_token = 'c1ae964f6c85b5a356a205e12a0ae7df'
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
    'conversation_started': False,
    'conversation_ended': False, #Added this new line if bot is asking again
    'Language': '' # Default language set to English 
}

# Initialize translator
subscription_key = "476bd55d5df04703a105bfb0595ce885"
endpoint = "https://api.cognitive.microsofttranslator.com/"
location = "eastus"

path = '/translate'
constructed_url = endpoint + path

params = {
    'api-version': '3.0',
    'from': '',
    'to': []
}
constructed_url = endpoint + path

headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

def translate_text(text, dest_language):
    # Translate the text to the destination language

    # Check if destination language is assigned
    if dest_language:
        # Translate the text to the destination language
        body = [{
            'text': text
        }]
        params['to'] = [dest_language]  # Set the destination language
        params['from'] = 'en'
        request = requests.post(constructed_url, params=params, headers=headers, json=body)
        response = request.json()
        return response[0]['translations'][0]['text']
    else:
        # If no language is assigned, return the original text
        return f"{text} : No Translation Language Detected!"
    
# Microsoft Language Detector
def detect_language(text):
    try:
        body = [{
            'text': text
        }]
        request = requests.post(constructed_url, params=params, headers=headers, json=body)
        response = request.json()
        return response[0]['detectedLanguage']['language']
    except:
        return None
    
# Local Language Detector
# def detect_language(text):
#     try:
#         return detect(text)
#     except:
#         return None

@api_view(['POST'])
def send_first_message(request):
    global conversation_state

    # Resetting conversation state for new chat
    conversation_state['Language'] = ''
    conversation_state['current_question_index'] = 0
    conversation_state['answers'] = {}
    conversation_state['conversation_started'] = True
    conversation_state['conversation_ended'] = False  # Reset the flag here
    conversation_state['Language'] = request.data.get('Language')

    name = request.data.get('name')
    hrname = request.data.get('hrname')
    phoneNo = request.data.get('phoneNo')
    JD = request.data.get('JobD')

    Comm_msg = f"Dear {name},\n\nI hope this message finds you well. My name is {hrname} and I am reaching out to you regarding your recent application with us.\n\nIn order to proceed with the next steps in our hiring process, we require some additional information from you. We have a few questions that will help us better understand your fitment for the role.\n\nYour prompt response will be greatly appreciated and will enable us to move forward with your application.\nThank you for your time and cooperation.\n\nBest regards, {hrname}\n\n Please Type Start. "
    li = [JD,Comm_msg]
    # Actual First Message Transfer
    for i in range(len(li)):
        message_body = li[i]
        translated_message_body = translate_text(message_body, conversation_state['Language'])  # Translate to conversation_state['Language']
        message = client.messages.create(body=translated_message_body, from_='whatsapp:+14155238886', to=phoneNo)
    
        print(message.sid)


    return HttpResponse(status=200)

@csrf_exempt
def whatsapp_webhook(request):
    if request.method == 'POST':
        # Get the incoming message data
        body = request.POST.get('Body', '')
        sender = request.POST.get('From', '')
        print(request.POST)

        # Check if the conversation has started
        if not conversation_state['conversation_started']:
            # If not, send the "Contact HR" message and return
            message = "Thank you for your time. Have a great day!\n\nContact HR for further queries."  # Later When database connected this can be converted for same candidate by storing his lang in database 
            # Translation Logic
            translated_message = translate_text(message, conversation_state['Language'])

            twiml_response = MessagingResponse()
            twiml_response.message(translated_message)
            return HttpResponse(str(twiml_response))

        # Process the incoming message
        response = process_message(body, sender)
        # Translate the response
        translated_response = translate_text(response, conversation_state['Language'])  # Translate


        # Create TwiML response
        twiml_response = MessagingResponse()
        twiml_response.message(translated_response)

        return HttpResponse(str(twiml_response))
    else:
        return HttpResponse(status=405)  # Method not allowed


def process_message(message, sender):
    global conversation_state

    user_language = detect_language(message)


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
        translated_next_question = translate_text(next_question, conversation_state['Language'])  # Translate to Given lang
        return translated_next_question
    else:
        # End of conversation, generate summary
        summary = generate_summary()
        # translated_summary = translate_text(summary, conversation_state['Language'])  # Translate to Spanish
        # return translated_summary
        # if user_language != conversation_state['Language']:
        #     translated_summary = translate_text(summary, conversation_state['Language'])
        #     return translated_summary
        # THis if loop can be removed
        return summary

def generate_summary():
    global conversation_state
    answers = conversation_state['answers']

    # Construct summary from answers
    summary = "Thank you for your answers:\n"
    for i, question in enumerate(questions):
        if detect_language(answers.get(i)) != conversation_state['Language']:
            summary += f"{question}\n- {translate_text(answers.get(i, 'No answer provided'),conversation_state['Language'])}\n"
        else:
             summary += f"{question}\n- {answers.get(i, 'No answer provided'),conversation_state['Language']}\n"

    # Reset conversation state for next interaction
    conversation_state['current_question_index'] = 0
    conversation_state['answers'] = {}
    conversation_state['conversation_ended'] = True
    conversation_state['conversation_started'] = False  # Reset the flag here
    
    return summary
