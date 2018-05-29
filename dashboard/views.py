# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests

from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader

from .models import Dialogue, Customer

from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

twilio_number = '+13237680838'
twilio_account_sid = 'AC27178f1decf817890c2b3b4884ea36b4'
twilio_auth_token = 'a18adaf2c0b9ec7a4ffde99f13f5e060'

azure_subscription_key = "4bdcbb7515e04552abc0c12a207927e7"
azure_sentiment_api_url = "https://westcentralus.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment"
azure_headers   = {"Ocp-Apim-Subscription-Key": azure_subscription_key}

def index(request):
    dialogue = None
    try:
        dialogue = Dialogue.objects.get(pk=1)
    except Dialogue.DoesNotExist:
        dialogue = Dialogue.default()
        dialogue.save()
    
    context = {'greeting': dialogue.greeting,
                'if_pos': dialogue.if_pos,
                'if_neg': dialogue.if_neg}
    return render(request, 'index.html', context)

# Create your views here.
def text(request):
    dialogue = get_object_or_404(Dialogue, pk=1)
    name = request.POST['name']
    product = request.POST['product']
    number = request.POST['number']
    customer = None
    try:
        customer = Customer.objects.get(phone_number=number)
    except Customer.DoesNotExist:
        customer = Customer(phone_number=number)
    customer.first_name = name
    customer.product_type = product
    customer.save()

    message = dialogue.greeting.replace("<firstName>", name).replace("<productType>", product)
    client = Client(twilio_account_sid, twilio_auth_token)

    send = client.messages.create(
                                  body=message,
                                  from_=twilio_number,
                                  to=number
                          )

    send.sid
    print(message)

    return HttpResponseRedirect(reverse('polls:index'))

@csrf_exempt
def sms_response(request):
    # Start our TwiML response
    resp = MessagingResponse()
    print("REQUEST:   "+str(request))
    message_received = request.POST['Body']
    from_number = request.POST['From']
    customer = Customer.objects.get(phone_number=from_number)
    name = customer.first_name
    prod = customer.product_type
    dialogue = get_object_or_404(Dialogue, pk=1)
    # Add a text message
    
    documents = {'documents' : [{'id': '1', 'language': 'en', 'text': message_received}]}
    response  = requests.post(azure_sentiment_api_url, headers=azure_headers, json=documents)
    sentiment = response.json()['documents'][0]['score']
    print("sentiment "+str(sentiment))
    if(sentiment<0.5):
        msg = dialogue.if_neg.replace("<firstName>", name).replace("<productType>", prod)
        resp.message(msg)
    else:
        msg = dialogue.if_pos.replace("<firstName>", name).replace("<productType>", prod)
        resp.message(msg)

 
    return HttpResponse(str(resp))

def edit(request, msg):
    dialogue = Dialogue.objects.get(pk=1)
    message = request.POST['message']

    if(msg == "1"):
        dialogue.greeting = message;
    elif(msg == "2"):
        dialogue.if_pos = message;
    elif(msg == "3"):
        dialogue.if_neg = message;
    dialogue.save()
    return HttpResponseRedirect(reverse('polls:index'))

def detail(request, question_id):
    question = Question.objects.get(pk=question_id)
    context = {'question': question}
    return render(request, 'detail.html', context)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)



def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))