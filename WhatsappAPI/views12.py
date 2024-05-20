import requests
import uuid
import json
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
auth_token = 'd3e5ba3d6b2cc012540335f308b7c38d'
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
    'conversation_ended': False,
    'Language': ''
}

# Initialize translator
subscription_key = ""
endpoint = ""
location = "eastus"

path = '/translate'
constructed_url = endpoint + path

params = {
    'api-version': '3.0',
    'from': '',
    'to': []
}

headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

def translate_text(text, dest_language):
    if dest_language:
        body = [{'text': text}]
        params['to'] = [dest_language]
        params['from'] = 'en'
        response = requests.post(constructed_url, params=params, headers=headers, json=body)
        response_data = response.json()
        return response_data[0]['translations'][0]['text']
    else:
        return f"{text} : No Translation Language Detected!"

def detect_language(text):
    try:
        body = [{'text': text}]
        response = requests.post(constructed_url, params=params, headers=headers, json=body)
        response_data = response.json()
        return response_data[0]['detectedLanguage']['language']
    except:
        return None

@api_view(['POST'])
def send_first_message(request):
    global conversation_state

    # Resetting conversation state for new chat
    conversation_state['Language'] = ''
    conversation_state['current_question_index'] = 0
    conversation_state['answers'] = {}
    conversation_state['conversation_started'] = True
    conversation_state['conversation_ended'] = False
    conversation_state['Language'] = request.data.get('Language')

    name = request.data.get('name')
    hrname = request.data.get('hrname')
    phoneNo = request.data.get('phoneNo')
    JD = request.data.get('JobD')

    Comm_msg = (f"Dear {name},\n\nI hope this message finds you well. My name is {hrname} and I am reaching out to you "
                "regarding your recent application with us.\n\nIn order to proceed with the next steps in our hiring process, "
                "we require some additional information from you. We have a few questions that will help us better understand "
                "your fitment for the role.\n\nYour prompt response will be greatly appreciated and will enable us to move "
                "forward with your application.\nThank you for your time and cooperation.\n\nBest regards, {hrname}\n\n Please Type Start. ")

    li = [JD, Comm_msg]
    for message_body in li:
        translated_message_body = translate_text(message_body, conversation_state['Language'])
        message = client.messages.create(body=translated_message_body, from_='whatsapp:+14155238886', to=phoneNo)
        print(message)

    return HttpResponse(status=200)

@csrf_exempt
def whatsapp_webhook(request):
    if request.method == 'POST':
        body = request.POST.get('Body', '')
        sender = request.POST.get('From', '')
        print(request.POST)

        if not conversation_state['conversation_started']:
            message = "Thank you for your time. Have a great day!\n\nContact HR for further queries."
            translated_message = translate_text(message, conversation_state['Language'])

            twiml_response = MessagingResponse()
            twiml_response.message(translated_message)
            return HttpResponse(str(twiml_response))

        response = process_message(body, sender)
        translated_response = translate_text(response, conversation_state['Language'])

        twiml_response = MessagingResponse()
        twiml_response.message(translated_response)

        return HttpResponse(str(twiml_response))
    else:
        return HttpResponse(status=405)

def process_message(message, sender):
    global conversation_state

    user_language = detect_language(message)

    if conversation_state['conversation_ended']:
        return "Thank you for your time. Have a great day!"

    current_question_index = conversation_state['current_question_index']
    conversation_state['answers'][current_question_index] = message

    if current_question_index < len(questions) - 1:
        conversation_state['current_question_index'] += 1
        next_question = questions[current_question_index + 1]
        if next_question == "What is your expected CTC?":
            if int(message) > 350000:
                return translate_text("Are you willing to negotiate?", conversation_state['Language'])
        elif next_question == "What is your notice period (In days)?":
            if int(message) > 30:
                return translate_text("We can have a maximum 30 days notice only. Can you manage it?", conversation_state['Language'])
        elif next_question == "What is your current location?":
            if message.lower() != "pune":
                return translate_text("Are you willing to relocate to Pune?", conversation_state['Language'])

        return translate_text(next_question, conversation_state['Language'])
    else:
        summary = generate_summary()
        return summary

def generate_summary():
    global conversation_state
    answers = conversation_state['answers']

    summary = "Thank you for your answers:\n"
    for i, question in enumerate(questions):
        if detect_language(answers.get(i)) != conversation_state['Language']:
            summary += f"{question}\n- {translate_text(answers.get(i, 'No answer provided'), conversation_state['Language'])}\n"
        else:
            summary += f"{question}\n- {answers.get(i, 'No answer provided')}\n"

    conversation_state['current_question_index'] = 0
    conversation_state['answers'] = {}
    conversation_state['conversation_ended'] = True
    conversation_state['conversation_started'] = False

    return summary
