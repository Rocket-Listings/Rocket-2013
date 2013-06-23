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

		sender    = request.POST.get('sender')
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

