import json
from listings.models import Listing, ListingPhoto, Buyer, Offer, Message, ListingCategory, ListingSpecKey, ListingSpecValue
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime, timedelta
from listings.forms import ListingForm, ListingPics
from django.contrib.auth.decorators import login_required
from ajaxuploader.views import AjaxFileUploader
from django.shortcuts import render, redirect, get_object_or_404
#from ListingsLocalUploadBackend import ListingsLocalUploadBackend
from listings.upload_backend import ProductionUploadBackend, DevelopmentUploadBackend
from django.utils import simplejson
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from rocket import get_client_ip
from django.db.models import Max
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest
import requests
import re
from bs4 import BeautifulSoup
from operator import __add__
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery
from django.core.urlresolvers import reverse
# Moved here from users/views.py

@login_required
def user_listings(request, username=None):
	user = request.user # if no username parameter is passed, defaults to the currently logged in user.
	if username:
		user = get_object_or_404(User, username=username)
	listings = Listing.objects.filter(user=user).order_by('-pub_date')[:10]
	buyers = Buyer.objects.filter(listing__user=user)
	messages = Message.objects.filter(listing__user=user)
	return render(request, 'listings/listings_dashboard.html', {'listings': listings, 'buyers': buyers, 'messages':messages,})

@login_required
def dashboard(request):
	sqs = SearchQuerySet().all()
	print sqs
	user = request.user
	listings = Listing.objects.filter(user=user).order_by('-pub_date').all() # later on we can change how many are returned
	buyers = reduce(__add__, map(lambda l: list(l.buyer_set.all()), listings), [])
	messages = reduce(__add__, map(lambda b: list(b.message_set.all()), buyers), [])
	return render(request, 'listings/listings_dashboard.html',  {'listings': listings, 'buyers': buyers, 'messages':messages})

def latest(request):
	listings = Listing.objects.all().order_by('-pub_date')[:10]
	return render(request, 'listings/listings_latest.html', {'listings': listings,})


def create(request):
	if request.method == 'GET':
		profile = request.user.get_profile()
		defaults = {'location':profile.location, 'category':profile.default_category, 'listing_type':profile.default_listing_type}
		form = ListingForm(initial=defaults)
		categories = ListingCategory.objects.all() #get all of the category information from database for tab view in listings_edit
		specs = ListingSpecKey.objects.all() #get all of the specs information from database for table insertion
		return render(request, 'listings/listing_create.html', {'form':form , 'categories':categories, 'specs':specs})

	elif request.method == 'POST':
		categories = ListingCategory.objects.all() #get categories if post request fails
		count = request.POST.get('final_count', 0) # get the final count name tag which contains the final photo count
		count = int(count)
		d={} # empty dictionary

		for x in range(0, count):
			d["photo{0}".format(x)] = request.POST.get(str(x)) # add photos into dictionary with the format photo.x = url[x]

		specCounter = 0 # begin the count to look through specs data
		specs = ListingSpecKey.objects.all() # grab all of specs

		listing_form = ListingForm(request.POST)

		if listing_form.is_valid():
			listing = listing_form.save(commit=False)
			listing.user = request.user
			listing.save()
			for x in range(0, count):
				string = d["photo%d" %(x)]
				photoDict = {'url': string, 'order': x, 'listing': listing}
				photo = ListingPhoto(**photoDict)
				photo.clean()
				photo.save()


			cat = str(request.POST.get('final_cat')) #get final category chosen
			postRequest = str(request.POST)
			matches = re.findall(r''+cat+'_\w+', postRequest) # find all category inputs matching the category
			for match in matches:
				while (str(specs[specCounter].category).split()[0] != cat):
					specCounter = specCounter + 1
					if specCounter>300:
						break
				if str(specs[specCounter].category).split()[0] == cat:
					infoSpec =  request.POST.get(match)
					specDict = {'name': infoSpec, 'key': specs[specCounter], 'listing': listing}
					specific = ListingSpecValue(**specDict)
					specific.clean()
					specific.save()
					specCounter = specCounter + 1


			if request.user.is_authenticated():
				return redirect(listing)
			else:
				return redirect(listing)
				# Do something for anonymous users.
		else:
			return render(request, 'listings/listing_create.html', {'form': ListingForm(request.POST), 'categories':categories, 'specs':specs})

def detail(request, listing_id):
	if request.method == 'GET':
		listing = get_object_or_404(Listing, id=listing_id)
		profile = request.user.get_profile()
		defaults = {'location':listing.location, 'category':listing.category, 'listing_type':profile.default_listing_type}
		form = ListingForm(initial=defaults)
		categories = ListingCategory.objects.all()
		photos = listing.listingphoto_set.all()
		specs = ListingSpecKey.objects.all()
		specifications = listing.listingspecvalue_set.all()
		return render(request, 'listings/listing_details.html', {'listing':listing, 'form':form, 'categories':categories, 'photos':photos, 'specs':specs, 'specifications':specifications})

	elif request.method == 'POST':
		listing = get_object_or_404(Listing, id=listing_id)
		if request.user == listing.user: # updating his own listing
			listing_form = ListingForm(request.POST, instance = listing)		
			if listing_form.is_valid():
				listing = listing_form.save()
				return redirect(listing)
			else:
				return render(request, 'listings/listing_update.html', {'form': listing_form})

def embed(request, listing_id):
	listing = get_object_or_404(Listing, id=listing_id)
	photos = ListingPhoto.objects.filter(listing=listing).order_by('order')

	# provide `url` and `thumbnail_url` for convenience.
	photos = map(lambda photo: {'url':photo.url, 'order':photo.order}, photos)
	return render(request, 'listings/listing_cl_embed.html', {'listing':listing, 'photos':photos})

@login_required
def update(request, listing_id):
	listing = get_object_or_404(Listing, id=listing_id)

	profile = request.user.get_profile()
	defaults = {'location':listing.location, 'category':listing.category, 'listing_type':profile.default_listing_type}
	form = ListingForm(initial=defaults)
	categories = ListingCategory.objects.all()
	photos = listing.listingphoto_set.all()
	specifications = listing.listingspecvalue_set.all()

	specs = ListingSpecKey.objects.all()
	categories = ListingCategory.objects.all()
	if request.user == listing.user: # updating his own listing
		if request.method == 'POST':
			listing_form = ListingForm(request.POST, instance = listing)
			if listing_form.is_valid():
				listing = listing_form.save()
				return redirect(listing, {'specs': specs, 'categories': categories})
			else:
				return render(request, 'listing_update.html', {'form': listing_form, 'specs': specs , 'categories': categories})
		else:
			return render(request, 'listing_update.html', {'listing':listing, 'form':form, 'categories':categories, 'photos':photos, 'specs':specs, 'specifications':specifications})
	else:
		return render(request, 'static_pages/403.html')

@login_required
def delete(request, listing_id):
	listing = get_object_or_404(Listing, id=listing_id)
	if request.user == listing.user:
		listing.delete()
		return redirect('listings.views.user_listings', username = request.user.username)


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
def listing_buyers_ajax(request, listing_id):
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

def message_thread_ajax(request, listing_id, buyer_id):
	listing = get_object_or_404(Listing, id=listing_id)
	buyer = get_object_or_404(Buyer, id=buyer_id)
	messages = listing.message_set.filter(buyer_id__exact=buyer_id).order_by('date')

	# if 'application/json' in request.META.get('HTTP_ACCEPT'):
	return HttpResponse(serializers.serialize("json", messages), mimetype='application/json')
	# else:
		# return HttpResponseBadRequest("Sorry please submit a good request")

def search(request):
	c = {}
	c.update(csrf(request))

	return render_to_response("listings/search_test.html",c)


def search_listings(request):
	if request.method == "POST":
		search_text = request.POST['search_text']
	else:
		search_text = ''

	if search_text == "" or search_text ==" ":
		listings = SearchQuerySet().all()
	else:
		listings = SearchQuerySet().autocomplete(content_auto=search_text)


	print "Posted"

	for listing in listings:
		listing.url_id = reverse('listings.views.detail', args=[str(listing.url_id)])

	return render_to_response('listings/partials/ajax_search.html', {'listings' : listings})

# Photo upload

# if not settings.DEBUG:
# 	upload_backend = ProductionUploadBackend
# else:
# 	upload_backend = DevelopmentUploadBackend


# import_uploader = AjaxFileUploader(backend=upload_backend)
