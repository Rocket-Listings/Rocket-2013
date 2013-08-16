from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives, BadHeaderError
from django.template.loader import render_to_string
from django.conf import settings
from celery.task import task
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from listings.models import Listing, Buyer, Message

import requests
import hashlib, urllib

@task(name='tasks.new_cl_admin_message_task')
def new_cl_admin_message_task(msg_dict):
	user = get_object_or_404(User, username=msg_dict['username'])
	listing = user.listing_set.get(title__exact=msg_dict['listing_title'])
	to_parse = BeautifulSoup(msg_dict['body'])
	manage_link = to_parse.find('a').contents[0]
	listing.CL_link = manage_link
	listing.status_id = 3
	listing.save()

	r = requests.get(manage_link)
	to_parse = BeautifulSoup(r.text)
	phone_page_text = "Your craigslist user account requires phone verification. Please use the form below to complete this process."
	try:
		if to_parse.find("section", class_="body").find("p").text == phone_page_text:
			buyer = Buyer(listing=listing, name="Apollo Rocket", email=settings.DEFAULT_FROM_EMAIL)
			buyer.save()
			message = Message(
				listing=listing, 
				buyer=buyer, 
				content="Sorry, but Craigslist wants you to verify your phone number. Follow this link to finish posting: " + activate_link)
			message.save()
	except AttributeError:
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
		view_link = to_parse.find('li').find_next('a').contents[0]
		listing.CL_view = view_link
		listing.save()

@task(name='tasks.send_message_task')
def send_message_task(message_id):
	msg = Message.objects.get(id=message_id)
	if msg.isSeller:
		from_name = msg.listing.user.get_profile().get_display_name()
		to_name = msg.buyer.name
		to_email = msg.buyer.email
		reply_email = "seller-" + msg.buyer.rocket_address + "@" + settings.MAILGUN_SERVER_NAME
	else:
		from_name = msg.buyer.name
		to_name = msg.listing.user.get_profile().get_display_name()
		to_email = msg.listing.user.email
		reply_email = "buyer-" + msg.buyer.rocket_address + "@" + settigns.MAILGUN_SERVER_NAME
	ctx = { 'from_name': from_name,
			'to_name': to_name,
			'content': msg.content,
			'date': msg.date,
			'listing_title': msg.listing.title,
			'toBuyer': msg.isSeller }
	subject = render_to_string('mail/dashboard_message_subject.txt', ctx)
	subject = ''.join(subject.splitlines()) # remove new lines
	message_text = render_to_string('mail/dashboard_message_plain.txt', ctx)
	message_html = render_to_string('mail/dashboard_message_html.html', ctx)
	mail_headers = {'Reply-To': from_name + "<" + reply_email + ">"}
	email = EmailMultiAlternatives(subject, message_text, 
		from_name + "<" + settings.DEFAULT_FROM_EMAIL + ">", 
		[to_name +  "<" + to_email + ">"], 
		headers=mail_headers)
	email.attach_alternative(message_html, "text/html")
	try:
		email.send()
	except BadHeaderError:
		return 'Invalid header found.'
	return msg.id
