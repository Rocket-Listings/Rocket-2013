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
def on_incoming_message(request):
	if request.method == 'POST':
		print "post recieved"

		sender    = request.POST.get('sender')
		print sender, len(sender)

		recipient = request.POST.get('recipient')
		print recipient, len(recipient)

		subject   = request.POST.get('subject', '')
		print subject, len(subject)

		frm = request.POST.get('from', '')
		print frm, len(frm)

		body = request.POST.get('body-plain', '')
		body_html = request.POST.get('body-html', '')
		text = request.POST.get('stripped-text', '')


		signature = request.POST.get('stripped-signature', '')
		timestamp = request.POST.get('timestamp', '')
		token = request.POST.get('token', '')
		sig = request.POST.get('signature', '')
		print signature, len(signature)

	
	if verify(token, timestamp, sig):
		print "verified"

		if str(sender).startswith('bounce-post'):
			"""Handles administrative emails from craigslist"""

			print "is @craigslist"
			print sender
			print frm
			user = get_object_or_404(User, username= recipient.split('@')[0])
			listing = user.listing_set.get(title__exact= subject.partition('"')[2].partition('"')[0])
			email = user.email
			print send_mail( subject , body, 'rocket@rocketlistings.mailgun.org', [email], fail_silently=False)

			message = Message(listing = listing, content = body, buyer = listing.buyer_set.get(name__exact = "Craigslist"))
			message.save()
			m = mailgun(recipient = recipient, sender = sender, frm = frm, subject = subject, body = body, text = text, 
			signature = signature, timestamp = timestamp, token = token, sig = sig)
			m.save()

			return HttpResponse('OK')

		elif str(sender).partition('@')[2] == 'example.com': #temporary to test  webhook
			m = mailgun(recipient = recipient, sender = sender, frm = frm, subject = subject, body = body, text = text, 
			signature = signature, timestamp = timestamp, token = token, sig = sig)
			m.save()
			return HttpResponse('OK')

		elif str(sender).startswith('bounce-anon'):
			"""Handles emails from anonomized cl buyers"""

			print "is @sale.craigslist.org"
			user = get_object_or_404(User, username= recipient.split('@')[0])
			listing = user.listing_set.get(title__exact= subject.partition(' - ')[0])
			buyer = re.findall(r'"(.*?)"', frm)
			buyer_email = re.findall(r'<(.*?)>', frm)
			print type(buyer)

			buyers = listing.buyer_set.all()

			for buy in buyers:
				print buy.name == str(buyer)
				
				if buy.name == str(buyer):
					break
			else:
				b = Buyer(listing = listing, name = buyer)#create a "buyer" to recieve cl messages
				b.save()

			print body, buyer
			

			message = Message(listing = listing, content = body, buyer = listing.buyer_set.get(name__exact = buyer))
			message.save()
			m = mailgun(recipient = recipient, sender = sender, frm = frm, subject = subject, body = body, text = text, 
			signature = signature, timestamp = timestamp, token = token, sig = sig)
			m.save()

			return HttpResponse('OK')


	else:
		print "didnt work"
		return HttpResponse('Unauthorized')
