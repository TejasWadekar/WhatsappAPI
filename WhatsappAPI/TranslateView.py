from django.http import HttpResponse
from twilio.twiml.messaging_response import MessagingResponse
from django_twilio.decorators import twilio_view
from google.cloud import translate_v2 as translate
import phonenumbers
import pycountry
from .models import QusAns

def translate_message(text, target_language):
    # Replace 'YOUR_API_KEY' with your Google Cloud API key
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    translated_text = result["translatedText"]
    return translated_text

def get_language_from_country_code(country_code):
    try:
        country = pycountry.countries.get(alpha_2=country_code)
        language = pycountry.languages.get(alpha_2=country.languages[0])
        return language.alpha_2
    except:
        # Default to English if country code is not recognized
        return "en"


questions = [
    "What is your current CTC?",
    "What is your expected CTC?",
    "What is your notice period (In days)?",
    "What is your current location?",
    "Are you willing to relocate?"
]

ListAns = []
ListQs = []

@twilio_view
def whatsAppWebhook(request):
    session_data = request.session
    current_question_index = session_data.get('current_question_index', 0)

    incoming_msg = request.POST.get('Body', '').strip().lower()
    sender_phone = request.POST.get('From', '')

    resp = MessagingResponse()

    if current_question_index < len(questions):
        current_question = questions[current_question_index]

        # Detect country code from sender's phone number
        phone_number = phonenumbers.parse(sender_phone)
        countrycode = phonenumbers.format_number(phone_number.country_code, phonenumbers.PhoneNumberFormat.E164)

        Lang = get_language_from_country_code(country_code=countrycode)

        # Translate incoming message to the language associated with sender's country code
        
        translated_incoming_msg = translate_message(incoming_msg, Lang)

        ListAns.append(translated_incoming_msg)

        # inserting into database
        # Profile.objects.create(phone_number=sender_phone, question=current_question, answer=translated_incoming_msg)

        session_data['current_question_index'] = current_question_index + 1

        if current_question_index < len(questions) - 1:
            next_question = questions[current_question_index + 1]
            resp.message(translate_message(next_question, Lang))
            ListQs.append(translate_message(next_question, Lang))

        else:
            resp.message("Thank you for providing the information. We will get back to you soon.")
    else:
        resp.message("Thank you for your message.")
    
    # inserting into database
    QusAns.objects.create(phone=phone_number,QA='\n'.join(ListAns, ','))
    
    return HttpResponse(str(resp))
