from mail.models import mailgun
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import hashlib, hmac
from django.core.mail import send_mail
from django.contrib.auth.models import User
from users.models import UserProfile
from django.shortcuts import render, redirect, get_object_or_404



# this function secures the webhook by:
# Concatenating timestamp and token values.
# Encoding the resulting string with the HMAC algorithm (using your API Key as a key and SHA256 digest mode).
# Comparing the resulting hexdigest to the signature.
def verify(token, timestamp, signature):
	api_key = 'key-9flqj538z-my-qcnpc74c2wit4vibl-3'
	return signature == hmac.new(
                             key=api_key,
                             msg='{}{}'.format(timestamp, token),
                             digestmod=hashlib.sha256).hexdigest()

@csrf_exempt
def on_incoming_message(request):
	if request.method == 'POST':
		sender    = request.POST.get('sender')
		recipient = request.POST.get('recipient')
		subject   = request.POST.get('subject', '')
		frm = request.POST.get('from', '')
		body = request.POST.get('body-plain', '')
		text = request.POST.get('stripped-text', '')
		signature = request.POST.get('stripped-signature', '')
		timestamp = request.POST.get('timestamp', '')
		token = request.POST.get('token', '')
		sig = request.POST.get('signature', '')

	if sender == 'robot@craigslist.org':
		name = recipient.split('@')[0]
		user = get_object_or_404(User, username=name)
		email = user.email
		send_mail( subject , body, 'postmaster@rocketlistings.mailgun.org', [email], fail_silently=False)
		return HttpResponse('OK')

	elif verify(token, timestamp, sig):
		m = mailgun(recipient = recipient, sender = sender, frm = frm, subject = subject, body = body, text = text, 
		signature = signature, timestamp = timestamp, token = token, sig = sig)
		m.save()
		return HttpResponse('OK')
	else:
		return HttpResponse('Unauthorized')
