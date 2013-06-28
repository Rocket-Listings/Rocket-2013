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

	# Todo: implement sessions and location.
	listing = get_object_or_404(Listing, id=listing_id)
	photos = ListingPhoto.objects.filter(listing=listing).order_by('order')

	try:
		b = Buyer.objects.get(listing= listing, name= "Craigslist")
	except ObjectDoesNotExist:
		b = Buyer(listing = listing, name = "Craigslist", email = "robots@craigslist.org")
		b.save()
	
	r = requests.get('https://post.craigslist.org/c/brl?lang=en') #GET the url to post to
	post_url = r.url.split('?')[0] #split out the query string

#1st Post request at ?=type
#############################
	to_parse = BeautifulSoup(r.text) #instantiate the html parser
	tag = to_parse.find('input', type= "hidden") #select the input tag w/ hashed key/value
	hashed_key = tag.attrs['name']
	hashed_value = tag.attrs['value']
	payload = {'id': 'fso', hashed_key: hashed_value}#assemble payload. fs = for sale
	#need to figure our how to make above statement based on listing rather than hard-coded
	r = requests.post(post_url, data=payload)


#2st Post request at ?=cat
#############################
	to_parse = BeautifulSoup(r.text) #instantiate the html parser
	tag = to_parse.find('input', type= "hidden") #select the input tag w/ hashed key/value
	hashed_key = tag.attrs['name']
	hashed_value = tag.attrs['value']
	payload = {'id': '145', hashed_key: hashed_value}#assemble payload. 145 = cars
	#payload = {'id': listing.category.CL_id, hashed_key: hashed_value}
	r = requests.post(post_url, data=payload)#POST and Redirect


#3rd Post request at ?=edit
#############################
	to_parse = BeautifulSoup(r.text) #parse
	payload_tuples = [('id2', '1916x831X1916x635X1920x1200'), 
		  		('browserinfo', '%7B%0A%09%22plugins%22%3A%20%22'),
				('FromEMail',  request.user.username + '@rocketlistings.mailgun.org'), #enter your email here
				('ConfirmEMail', request.user.username + '@rocketlistings.mailgun.org'),
				('xstreet0', ''),
				('xstreet1', ''),
				('city', ''),
				('region', ''),
				('postal', ''),
				('go', 'Continue')] #intial (staticish) payload data. Using a list of tuples b/c it is mutable but easily converted into a dict


	#Still parsing
	title_id = to_parse.find("span", text= "posting title:").next_sibling.contents[1].attrs['name']
	payload_tuples += [(title_id, listing.title)] 

	price_id = to_parse.find("span", text= "price:").next_sibling.contents[1].attrs['name']
	payload_tuples += [(price_id, listing.price)]

	location_id = to_parse.find("span", text= "specific location:").next_sibling.contents[0].attrs['name']
	payload_tuples += [(location_id, listing.location)]

	anon_id = to_parse.find("label", title= "craigslist will anonymize your email address").contents[1].attrs['name']
	payload_tuples += [(anon_id, 'C')]

	description_id = to_parse.find("textarea", cols="80").attrs['name']
	payload_tuples += [(description_id, listing.description)]

	hashed_key = to_parse.find('input', type= "hidden").attrs['name']
	hashed_value = to_parse.find('input', type= "hidden").attrs['value']

	payload_tuples += [(hashed_key, hashed_value)]

	payload = dict(payload_tuples) #assemble Payload

	r = requests.post(post_url, data=payload) #POST and Redirect


#4th Post request at ?=editimage
#############################
	to_parse = BeautifulSoup(r.text) # you should get the pattern by now :)

	#Upload POST
	payload_tuples = [('go', 'add image')]
	hashed_key = to_parse.find('form', enctype="multipart/form-data").contents[1].attrs['name']
	hashed_value = to_parse.find('form', enctype="multipart/form-data").contents[1].attrs['value']
	payload_tuples += [(hashed_key, hashed_value)]
	payload_tuples += [(to_parse.find('form', enctype="multipart/form-data").contents[1].contents[1].attrs['name'], 'add')]

	payload = dict(payload_tuples)

	for photo in photos:
		r = requests.post(post_url, files = dict([('file', ('photo', open( 'media/' +photo.url, 'rb')))]), data=payload)
		print "uploading photo" + photo.url


	# submit POST
	to_parse = BeautifulSoup(r.text)
	payload_tuples = [('go', 'Done With Images')]
	hashed_key = to_parse.find_all('form')[1].contents[1].attrs['name']
	hashed_value = to_parse.find_all('form')[1].contents[1].attrs['value']
	payload_tuples += [(hashed_key, hashed_value), (hashed_key, hashed_value)] #for some reason cl posts this twice
	payload_tuples += [(to_parse.find_all('form')[1].contents[1].contents[1].attrs['name'], 'fin')]

	payload = dict(payload_tuples)
	r = requests.post(post_url, data=payload)

#5th Post request at ?=preview
#############################
	to_parse = BeautifulSoup(r.text)

	payload_tuples = [('go', 'Continue')]
	payload_tuples += [(to_parse.find('section', id="previewButtons").contents[1].contents[1].attrs['name'], to_parse.find('section', id="previewButtons").contents[1].contents[1].attrs['value'])]
	payload_tuples += [(to_parse.find('section', id="previewButtons").contents[1].contents[1].contents[1].attrs['name'], 'y')]

	payload = dict(payload_tuples)
	r = requests.post(post_url, data=payload)

	return render(request, 'listings_autopost.html',  {'listing': listing, 'debug': r.text})