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
		print "admin post recieved"

		user = get_object_or_404(User, username= request.POST.get('recipient').split('@')[0])
		listing = user.listing_set.get(title__exact= request.POST.get('subject', '').partition('"')[2].partition('"')[0])
		email = user.email
		send_mail( request.POST.get('subject', '') , request.POST.get('body-plain', ''), 'rocket@rocketlistings.mailgun.org', [email], fail_silently=False)
		message = Message(listing = listing, content = request.POST.get('body-plain', ''), buyer = listing.buyer_set.get(name__exact = "Craigslist"))
		message.save()

	if verify(request.POST.get('token', ''), request.POST.get('timestamp', ''), request.POST.get('signature', '')):
		return HttpResponse('OK')
	else:
		return HttpResponse('Unauthorized')


@csrf_exempt
def on_incoming_buyer_message(request):

	if request.method == 'POST':
		print "buyer post recieved"
		
		user = get_object_or_404(User, username= request.POST.get('recipient').split('@')[0])
		listing = user.listing_set.get(title__exact= request.POST.get('subject', '').partition(' - ')[0])

		print request.POST.get('message-headers')

		buyer_name = request.POST.get('from', '').partition("\"")[2].partition("\"")[0]
		buyer_email = request.POST.get('from', '').partition("<")[2].partition(">")[0]

		print buyer_email

		try:
			b = Buyer.objects.get(listing= listing, name= buyer_name)
			print "found buyer"
		except ObjectDoesNotExist:
			print "buyer not found--creating buyer"

			b = Buyer(listing = listing, name = buyer_name, email = buyer_email)
			b.save()

		print b

		
		#message = Message(listing = listing, content = body, buyer = listing.buyer_set.get(name__exact = buyer))
		#message.save()
		#m = mailgun(recipient = recipient, sender = sender, frm = frm, subject = subject, body = body, text = text, 
		#signature = signature, timestamp = timestamp, token = token, sig = sig)
		#m.save()




		#buyers = listing.buyer_set.all()

		#for buy in buyers:
			#print buy.name == str(buyer)
			
			#if buy.name == str(buyer):
				#break
		#else:
			#b = Buyer(listing = listing, name = buyer)#create a "buyer" to recieve cl messages
			#b.save()

		#print body, buyer
		

		#message = Message(listing = listing, content = body, buyer = listing.buyer_set.get(name__exact = buyer))
		#message.save()
		#m = mailgun(recipient = recipient, sender = sender, frm = frm, subject = subject, body = body, text = text, 
		#signature = signature, timestamp = timestamp, token = token, sig = sig)
		#m.save()

	if verify(request.POST.get('token', ''), request.POST.get('timestamp', ''), request.POST.get('signature', '')):
		print "verified"
		return HttpResponse('OK')

	else:
		print "not verified"
		return HttpResponse('Unauthorized')