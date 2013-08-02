from mail.models import mailgun
from listings.models import Message, Buyer, Listing
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import hashlib, hmac
from django.core.mail import send_mail
from django.contrib.auth.models import User
from users.models import UserProfile
from django.shortcuts import render, redirect, get_object_or_404
import re
from django.core.exceptions import ObjectDoesNotExist
from listings.models import Listing, ListingPhoto, Buyer, Offer, Message 
from django.contrib.auth.models import User
import requests
from bs4 import BeautifulSoup
from mail.tasks import autopost_task




def verify(token, timestamp, signature):
	"""this function secures the webhook by:
	Concatenating timestamp and token values.
	Encoding the resulting string with the HMAC algorithm (using your API Key as a key and SHA256 digest mode).
	Comparing the resulting hexdigest to the signature."""

	api_key = 'key-9flqj538z-my-qcnpc74c2wit4vibl-3'
	return signature == hmac.new(
                             key=api_key,
                             msg='{}{}'.format(timestamp, token),
                             digestmod=hashlib.sha256).hexdigest()

@csrf_exempt
def on_incoming_test_message(request):
	if request.method == 'POST':
		print "post recieved"
		mime = request.POST.get('message-headers')
		print mime
		sender = request.POST.get('sender')
		print sender
		recipient = request.POST.get('recipient')
		print recipient
		subject   = request.POST.get('subject', '')
		print subject
		frm = request.POST.get('from', '')
		print frm
		body = request.POST.get('body-plain', '')
		print body
		body_html = request.POST.get('body-html', '')
		print body_html
		text = request.POST.get('stripped-text', '')
		print text
		signature = request.POST.get('stripped-signature', '')
		print signature
		timestamp = request.POST.get('timestamp', '')
		token = request.POST.get('token', '')
		sig = request.POST.get('signature', '')

	if verify(token, timestamp, sig):
		print "verified"
		return HttpResponse('OK')

	else:
		print "not verified"
		return HttpResponse('Unauthorized')


@csrf_exempt
def on_incoming_admin_message(request):

	if request.method == 'POST':
		# user = get_object_or_404(User, username= request.POST.get('recipient').split('@')[0])
		# listing = user.listing_set.get(title__exact= request.POST.get('subject', '').partition('"')[2].partition('"')[0])
		# email = user.email
		# send_mail( request.POST.get('subject', '') , request.POST.get('body-html', ''), 'rocket@rocketlistings.mailgun.org', [email], fail_silently=False)
		to_parse = BeautifulSoup(request.POST.get('body-html', ''))
		activate_link = to_parse.find('a').contents[0]
		r = requests.get(activate_link)

		to_parse = BeautifulSoup(r.text)
		form = to_parse.find('form')
		action = form.attrs['action']
		hidden_inputs = form.find_all_next('input', type='hidden', limit=2)
		hashed_key_1 = hidden_inputs[0].attrs['name']
		hashed_value_1 = hidden_inputs[0].attrs['value']
		hashed_key_2 = hidden_inputs[1].attrs['name']
		hashed_value_2 = hidden_inputs[1].attrs['value']
		payload = {hashed_key_1: hashed_value_1, hashed_key_2: hashed_value_2}
		r = requests.post(action, data=payload)

		to_parse = BeautifulSoup(r.text)
		print to_parse
		cl_url = to_parse.find('li').find_next('a').contents[0]
		print cl_url

		#message = Message(listing = listing, content = cleaned_content, buyer = listing.buyer_set.get(name__exact = "Craigslist"))
		#message.save()

	if verify(request.POST.get('token', ''), request.POST.get('timestamp', ''), request.POST.get('signature', '')):
		return HttpResponse('OK')
	else:
		return HttpResponse('Unauthorized')


@csrf_exempt
def on_incoming_buyer_message(request):

	if request.method == 'POST':

		user = get_object_or_404(User, username= request.POST.get('recipient').split('@')[0])
		listing = user.listing_set.get(title__exact= request.POST.get('subject', '').partition(' - ')[0])
		buyer_name = request.POST.get('from', '').partition("\"")[2].partition("\"")[0]
		buyer_email = request.POST.get('from', '').partition("<")[2].partition(">")[0]

		try:
			b = Buyer.objects.get(listing= listing, name= buyer_name)
		except ObjectDoesNotExist:
			b = Buyer(listing = listing, name = buyer_name, email = buyer_email)
			b.save()

		message = Message(listing = listing, content = request.POST.get('body-plain', ''), buyer = b)
		message.save()

	if verify(request.POST.get('token', ''), request.POST.get('timestamp', ''), request.POST.get('signature', '')):
		return HttpResponse('OK')
	else:
		return HttpResponse('Unauthorized')

def autopost(request, listing_id):
	username = User.objects.get(username=request.user).username
	result = autopost_task.delay(username, listing_id)
	return HttpResponse()

def send_message(request, message_id):
	send_message_task.delay(message_id)
	return HttpResponse()
