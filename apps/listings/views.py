from listings.models import Listing, ListingPhoto, Buyer, Offer, Message, ListingCategory 
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime, timedelta
from listings.forms import ListingForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ajaxuploader.views import AjaxFileUploader
#from ListingsLocalUploadBackend import ListingsLocalUploadBackend
from listings.upload_backend import ProductionUploadBackend, DevelopmentUploadBackend
from django.utils import simplejson
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from rocketlistings import get_client_ip
from django.db.models import Max
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest
import requests
from bs4 import BeautifulSoup



# Moved here from users/views.py

@login_required
def user_listings(request, username=None):
	user = request.user # if no username parameter is passed, defaults to the currently logged in user.
	if username:
		user = get_object_or_404(User, username=username)
	listings = Listing.objects.filter(user=user).order_by('-pub_date')[:10]
	return render(request, 'user_overview.html', {'listings': listings})

@login_required
def dashboard(request, username=None):
	user = request.user # if no username parameter is passed, defaults to the currently logged in user.
	if username:
		user = get_object_or_404(User, username=username)
	listings = Listing.objects.filter(user=user).order_by('-pub_date')[:10]
	return render(request, 'listings_dashboard.html', {'listings': listings})

def latest(request):
	listings = Listing.objects.all().order_by('-pub_date')[:10]
	return render(request, 'listings_latest.html', {'listings': listings,})


def create(request):
	if request.method == 'GET':
		profile = request.user.get_profile()
		defaults = {'location':profile.location, 'category':profile.default_category, 'listing_type':profile.default_listing_type}
		form = ListingForm(initial=defaults)
		categories = ListingCategory.objects.all()
		return render(request, 'listing_create.html', {'form':form , 'categories': categories})

	elif request.method == 'POST':
		listing_form = ListingForm(request.POST)
		if listing_form.is_valid():
			listing = listing_form.save(commit=False)
			listing.user = request.user
			listing.save()
			if request.user.is_authenticated():
				return redirect(listing)
			else:
				return redirect(listing)
				# Do something for anonymous users.
		else:
			return render(request, 'listing_create.html', {'form': ListingForm(request.POST),})

def detail(request, listing_id):
	if request.method == 'GET':
		listing = get_object_or_404(Listing, id=listing_id)
		profile = request.user.get_profile()
		defaults = {'location':listing.location, 'category':listing.category, 'listing_type':profile.default_listing_type}
		form = ListingForm(initial=defaults)
		return render(request, 'listing_details.html', {'listing':listing, 'form':form})
	elif request.method == 'POST':
		listing = get_object_or_404(Listing, id=listing_id)
		if request.user == listing.user: # updating his own listing
			listing_form = ListingForm(request.POST, instance = listing)		
			if listing_form.is_valid():
				listing = listing_form.save()
				return redirect(listing)
			else:
				return render(request, 'listing_update.html', {'form': listing_form})



def embed(request, listing_id):
	listing = get_object_or_404(Listing, id=listing_id)
	photos = ListingPhoto.objects.filter(listing=listing).order_by('order')

	# provide `url` and `thumbnail_url` for convenience.
	photos = map(lambda photo: {'url':photo.url, 'order':photo.order}, photos) 
	return render(request, 'listing_cl_embed.html', {'listing':listing, 'photos':photos})

@login_required
def update(request, listing_id):
	listing = get_object_or_404(Listing, id=listing_id)
	if request.user == listing.user: # updating his own listing
		if request.method == 'POST':
			listing_form = ListingForm(request.POST, instance = listing)		
			if listing_form.is_valid():
				listing = listing_form.save()
				return redirect(listing)
			else:
				return render(request, 'listing_update.html', {'form': listing_form})
		else:
			return render(request, 'listing_update.html', {'form':ListingForm(instance = listing),})
	else:
		return render(request, '403.html')

@login_required
def delete(request, listing_id):
	listing = get_object_or_404(Listing, id=listing_id)
	if request.user == listing.user:
		listing.delete()
		return redirect('listings.views.user_listings', username = request.user.username)

def offers(request, listing_id):
	listing = get_object_or_404(Listing, id=listing_id)
	offers = listing.offer_set.all()
	return render(request, 'listing_offers.html',  {'listing': listing, 'offers': offers,})

@csrf_exempt #this need to be changed but i cant be bothered to figure out the csrf stuff atm
def messages(request, listing_id):
	if request.method == "POST":

		listing = get_object_or_404(Listing, id=listing_id)
		buyerId = request.POST.get('buyer_id')
		buyer = get_object_or_404(Buyer, id=buyerId)
		content = request.POST.get('content')
		subject = ('New Message from ' + listing.user.userprofile.name) 

		send_mail( subject , content, 'postmaster@rocketlistings.mailgun.org', [buyer.email], fail_silently=False)

		m = Message(listing = listing, isSeller = True, buyer = buyer, content = content)
		m.save()


	listing = get_object_or_404(Listing, id=listing_id)
	buyers = listing.buyer_set.all().order_by('name')
	messages = listing.message_set.all().order_by('date')
	return render(request, 'listing_messages.html', {'listing': listing, 'messages':messages, 'buyers': buyers,})	

def delete_ajax(request, listing_id):
	response = {}
	try:
		listing = Listing.objects.get(id=listing_id)
	except ObjectDoesNotExist:
		response['success'] = False
		response['reason'] = 'Cannot find listing.'
	if request.user == listing.user:
		listing.delete()
		response['success']= True
	else:
		response['success'] = False
		response['reason'] = 'Cannot delete someone else\'s listings!'
	return HttpResponse(simplejson.dumps(response), content_type = 'application/javascript; charset=utf8')

### DASHBOARD

#this is my first api so I'm not gonna join the requests. If this is too slow
#it wont be too hard to redo
def ajax_listing_buyers(request, listing_id):
	'''Returns a list of Buyers associated with the listing id (of the logged in user)'''
	listing = get_object_or_404(Listing, id=listing_id)
	buyers = listing.buyer_set.all().order_by('name')

	for buyer in buyers:
		buyer.curMaxOffer =  buyer.max_offer()

	# if 'application/json' in request.META.get('HTTP_ACCEPT'):
	json = serializers.serialize("json", buyers)
	return HttpResponse(serializers.serialize("json", buyers), mimetype='application/json')
	# else:
		# return HttpResponseBadRequest("Sorry please submit a good request")

def ajax_message_thread(request, listing_id, buyer_id):
	listing = get_object_or_404(Listing, id=listing_id)
	buyer = get_object_or_404(Buyer, id=buyer_id)
	messages = listing.message_set.filter(buyer_id__exact=buyer_id).order_by('date')

	# if 'application/json' in request.META.get('HTTP_ACCEPT'):
	return HttpResponse(serializers.serialize("json", messages), mimetype='application/json')
	# else:
		# return HttpResponseBadRequest("Sorry please submit a good request")

# Photo upload

if settings.PRODUCTION:
	upload_backend = ProductionUploadBackend
else:
	upload_backend = DevelopmentUploadBackend


import_uploader = AjaxFileUploader(backend=upload_backend)


def autopost(request, listing_id):

	# Todo: implement sessions and location.
	listing = get_object_or_404(Listing, id=listing_id)
	photos = ListingPhoto.objects.filter(listing=listing).order_by('order')

	
	r = requests.get('https://post.craigslist.org/c/brl?lang=en') #GET the url to post to
	post_url = r.url.split('?')[0] #split out the query string

#1st Post request at ?=type
#############################
	to_parse = BeautifulSoup(r.text) #instantiate the html parser
	tag = to_parse.find('input', type= "hidden") #select the input tag w/ hashed key/value
	hashed_key = tag.attrs['name']
	hashed_value = tag.attrs['value']
	payload = {'id': 'fs', hashed_key: hashed_value}#assemble payload. fs = for sale
	r = requests.post(post_url, data=payload)


#2st Post request at ?=cat
#############################
	to_parse = BeautifulSoup(r.text) #instantiate the html parser
	tag = to_parse.find('input', type= "hidden") #select the input tag w/ hashed key/value
	hashed_key = tag.attrs['name']
	hashed_value = tag.attrs['value']
	payload = {'id': '169', hashed_key: hashed_value}#assemble payload. 169 = antiques
	r = requests.post(post_url, data=payload)#POST and Redirect


#3rd Post request at ?=edit
#############################
	to_parse = BeautifulSoup(r.text) #parse

	payload_tuples = [('id2', '1916x831X1916x635X1920x1200'), 
		  		('browserinfo', '%7B%0A%09%22plugins%22%3A%20%22'),
				('FromEMail', 'ofgeyizx@sharklasers.com'), #enter your email here
				('ConfirmEMail', 'ofgeyizx@sharklasers.com'),
				('xstreet0', ''),
				('xstreet1', ''),
				('city', ''),
				('region', ''),
				('postal', ''),
				('go', 'Continue')] #intial (staticish) payload data. Using a list of tuples b/c it is mutable but easily converted into a dict


	 #Still parsing
	title_id = to_parse.find("span", text= "Posting Title:").next_sibling.contents[1].attrs['name']
	payload_tuples += [(title_id, listing.title)] 

	price_id = to_parse.find("span", text= "Price:").next_sibling.contents[1].attrs['name']
	payload_tuples += [(price_id, listing.price)]

	location_id = to_parse.find("span", text= "Specific Location:").next_sibling.contents[0].attrs['name']
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

	fileslist = []
	for photo in photos:
		fileslist += [('file', ('photo', open( 'media/' +photo.url, 'rb')))]
	files = dict(fileslist)
	r = requests.post(post_url, files = files, data=payload)

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
	to_parse.prettify()

	payload_tuples = [('go', 'Continue')]
	payload_tuples += [(to_parse.find('form', style="float: right;").contents[1].attrs['name'], to_parse.find('form', style="float: right;").contents[1].attrs['value'])]
	payload_tuples += [(to_parse.find('form', style="float: right;").contents[1].contents[1].attrs['name'], to_parse.find('form', style="float: right;").contents[1].contents[1].attrs['value'])]

	payload = dict(payload_tuples)
	r = requests.post(post_url, data=payload)

	return render(request, 'listings_autopost.html',  {'listing': listing, 'debug': r.text})

