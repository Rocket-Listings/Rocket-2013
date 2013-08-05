from celery.task import task
from listings.models import Listing, Buyer, ListingPhoto
from bs4 import BeautifulSoup
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from celery.signals import task_sent
from celery.signals import task_success


@task(name='tasks.autopost_task')
def autopost_task(username, listing_id):

	# Todo: implement sessions and location.
	listing = get_object_or_404(Listing, id=listing_id)
	photos = ListingPhoto.objects.filter(listing=listing).order_by('order')

	# try:
	# 	b = Buyer.objects.get(listing= listing, name= "Craigslist")
	# except ObjectDoesNotExist:
	# 	b = Buyer(listing = listing, name = "Craigslist", email = "robots@craigslist.org")
	# 	b.save()
	
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
				('FromEMail',  username + '@rocketlistings.mailgun.org'), #enter your email here
				('ConfirmEMail', username + '@rocketlistings.mailgun.org'),
				('xstreet0', ''),
				('xstreet1', ''),
				('city', ''),
				('region', ''),
				('postal', ''),
				('go', 'Continue')] #intial (staticish) payload data. Using a list of tuples b/c it is mutable but easily converted into a dict


	#Still parsing
	title_id = to_parse.find("span", text="posting title:").find_next_sibling("input").attrs['name']
	payload_tuples += [(title_id, listing.title)] 

	price_id = to_parse.find("span", text="price:").find_next_sibling("input").attrs['name']
	payload_tuples += [(price_id, listing.price)]

	location_id = to_parse.find("span", text="specific location:").find_next_sibling("input").attrs['name']
	payload_tuples += [(location_id, listing.location)]

	anon_id = to_parse.find("label", title="craigslist will anonymize your email address").contents[1].attrs['name']
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
	payload_tuples += [(to_parse.find('form', enctype="multipart/form-data").contents[1].find_next_sibling("input").attrs['name'], 'add')]

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
	payload_tuples += [(to_parse.find_all('form')[1].contents[1].find_next_sibling("input").attrs['name'], 'fin')]

	payload = dict(payload_tuples)
	r = requests.post(post_url, data=payload)

#5th Post request at ?=preview
#############################
	to_parse = BeautifulSoup(r.text)

	payload_tuples = [('go', 'Continue')]
	payload_tuples += [(to_parse.find('section', id="previewButtons").contents[1].contents[1].attrs['name'], to_parse.find('section', id="previewButtons").contents[1].contents[1].attrs['value'])]
	payload_tuples += [(to_parse.find('section', id="previewButtons").contents[1].contents[1].find_next_sibling("input").attrs['name'], 'y')]

	payload = dict(payload_tuples)
	r = requests.post(post_url, data=payload)

	return Listing.objects.get(pk=listing_id).pk

@task_success.connect
def autopost_success_handler(sender=None, result=None, args=None, kwargs=None, **kwds):
	listing = Listing.objects.get(pk=result)
	listing.status_id = 3
	listing.save()

def send_message_task(message_id):
	pass
