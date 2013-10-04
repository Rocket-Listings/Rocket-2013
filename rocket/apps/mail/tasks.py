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
import mechanize
import hashlib, urllib

@task(name='tasks.new_cl_admin_message_task')
def new_cl_admin_message_task(msg_dict):
	print "entered admin task"
	user = get_object_or_404(User, username=msg_dict['username'])
	listing = user.listing_set.get(title__exact=msg_dict['listing_title'])
	to_parse = BeautifulSoup(msg_dict['body'])
	manage_link = to_parse.find('a').contents[0]
	print manage_link
	listing.CL_link = manage_link
	listing.status_id = 3
	listing.save()
	user.get_profile().subtract_credit()

	r = requests.get(manage_link)
	to_parse = BeautifulSoup(r.text)
	phone_page_text = "Your craigslist user account requires phone verification. Please use the form below to complete this process."
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
	try:
		if to_parse.find("section", class_="body").find("p").text == phone_page_text:
			buyer = Buyer(listing=listing, name="Apollo Rocket", email=settings.DEFAULT_FROM_EMAIL)
			buyer.save()
			message = Message(
				listing=listing, 
				buyer=buyer, 
				content="Sorry, but Craigslist wants you to verify your phone number. Follow this link to finish posting: " + manage_link)
			message.save()
	except AttributeError:
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

@task(name='tasks.lookup_view_links_task')
def lookup_view_links_task(*listing_ids):
	view_page_text = "Your posting can be seen at "
	for id in listing_ids:
		listing = Listing.objects.get(id=id)
		if listing.CL_link:
			r = requests.get(listing.CL_link)
			try:
				partition = BeautifulSoup(r.text).find("p").text.partition(view_page_text)
			except AttributeError:
				partition = BeautifulSoup(r.text).find("li").text.partition(view_page_text)
			if partition[1]:
				# Houston, we have a link!
				# Else, listing has not been activated so we do nothing
				listing.CL_view = partition[2].strip(".")
				listing.save()

@task(name='tasks.process_new_cl_message_task')
def process_new_cl_message_task(*args, **kwargs):
	"""
	Takes keyword arguments:
	'listing_view_link': The link in the original message
	'buyer_name': The name of the buyer from the original message
	'buyer_email': The email of the buyer from the original message
	'message_id': The id of the message saved without a buyer or listing
	"""

	listing = Listing.objects.get(CL_view=kwargs['listing_view_link'])
	try:
		buyer = Buyer.objects.get(listing=listing, name=kwargs['buyer_name'])
	except ObjectDoesNotExist:
		buyer = Buyer(listing=listing, name=kwargs['buyer_name'], email=kwargs['buyer_email'])
		buyer.save()

	message = Message.objects.get(id=kwargs['message_id'])
	message.buyer = buyer
	if not message.listing:
		message.listing = listing
	message.save()