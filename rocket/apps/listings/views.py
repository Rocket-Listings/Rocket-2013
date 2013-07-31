from listings.models import *
from listings import utils
import json
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime, timedelta
from listings.forms import ListingForm, SpecForm, ListingPhotoFormSet
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST 
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import simplejson
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from rocket import get_client_ip
from django.db.models import Max
from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest
from operator import __add__ as combine
from django.http import Http404
from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery
from django.core.urlresolvers import reverse
from haystack import connections
from users.decorators import first_visit, view_count
from django.template.response import TemplateResponse



@first_visit
@login_required
def dashboard(request):
	user = request.user
	listings = Listing.objects.filter(user=user).order_by('-pub_date').all() # later on we can change how many are returned
	buyers = reduce(combine, map(lambda l: list(l.buyer_set.all()), listings), [])
	messages = reduce(combine, map(lambda b: list(b.message_set.all()), buyers), [])
	return TemplateResponse(request, 'listings/dashboard.html',  {'listings': listings, 'buyers': buyers, 'messages':messages})


# @login_required
# def user_listings(request, username=None):
# 	user = request.user # if no username parameter is passed, defaults to the currently logged in user.
# 	if username:
# 		user = get_object_or_404(User, username=username)
# 	listings = Listing.objects.filter(user=user).order_by('-pub_date')[:10]
# 	buyers = Buyer.objects.filter(listing__user=user)
# 	messages = Message.objects.filter(listing__user=user)
# 	return TemplateResponse(request, 'listings/listings_dashboard.html', {'listings': listings, 'buyers': buyers, 'messages':messages})

@view_count
@first_visit
@login_required
def create(request, pane='edit'):
	if request.method == 'GET':
		profile = request.user.get_profile()
		defaults = {
			'location': profile.location, 
			'category': profile.default_category, 
			'listing_type': profile.default_listing_type,
		}
		cxt = {
			'form': ListingForm(initial=defaults),
			'pane': pane,
			'photo_formset': ListingPhotoFormSet(prefix="listingphoto_set")
		}
		cxt.update(utils.get_listing_vars())
		return TemplateResponse(request, 'listings/detail.html', cxt)
	else: # POST
		return update(request)

@login_required
@require_POST
def update(request, listing_id=None): # not directly addressed by a route, allows DRY listing saving
	if listing_id:
		listing = get_object_or_404(Listing, id=listing_id)
		if request.user != listing.user:
			raise Http404
	else:
		listing = Listing()

	listing_form = ListingForm(request.POST, instance=listing)
	specs = listing.listingspecvalue_set.select_related()
	spec_form = SpecForm(request.POST, initial=specs) # SpecForm is not a real form
	photo_formset = ListingPhotoFormSet(request.POST, instance=listing, prefix="listingphoto_set")
	if listing_form.is_valid() and spec_form.is_valid() and photo_formset.is_valid():
		listing = listing_form.save(commit=False)
		listing.user = request.user
		listing.save()
		for name, value in spec_form.cleaned_data.items():
			spec_id = int(name.replace('spec-',''))
			ListingSpecValue.objects.create(value=value, key_id=spec_id, listing_id=listing.id)
		photo_formset.save()
		return redirect(listing)
	else:
		print photo_formset.errors
		# preserving validation errors
		cxt = {
			'form': listing_form,
			'spec_form': spec_form,
			'pane': 'edit',
			'photo_formset': photo_formset
		}
		cxt.update(utils.get_listing_vars())
		return TemplateResponse(request, 'listings/detail.html', cxt)

@view_count
def detail(request, listing_id, pane='preview'):
	listing = get_object_or_404(Listing, id=listing_id)
	request.user.skip_count = listing.user == request.user
	
	if request.method == 'GET':
		if listing.user == request.user:
			form = ListingForm(instance=listing)
			
			# prep specs
			specs_set = listing.listingspecvalue_set.select_related().all()
			specs = {}
			for spec in specs_set:
				specs[spec.key_id] = spec
			spec_form = SpecForm(initial=specs)

			photo_formset = ListingPhotoFormSet(instance=listing, prefix="listingphoto_set")

			cxt = {
				'form': form,
				'spec_form': spec_form,
				'photo_formset': photo_formset,
				'pane': pane
			}
			cxt.update(utils.get_listing_vars())
			return TemplateResponse(request, 'listings/detail.html', cxt)
		else:
			specs = listing.listingspecvalue_set.select_related().all()
			photos = listing.listingphoto_set.all()
			cxt = {
				'listing': listing,
				'photos': photos,
				'specs': specs,
			}
			return TemplateResponse(request, 'listings/detail_public.html', cxt)
	else: # POST
		return update(request, listing_id)

def embed(request, listing_id):
	listing = get_object_or_404(Listing, id=listing_id)
	photos = ListingPhoto.objects.filter(listing=listing).order_by('order')

	# provide `url` and `thumbnail_url` for convenience.
	photos = map(lambda photo: {'url':photo.url, 'order':photo.order}, photos)
	return TemplateResponse(request, 'listings/cl_embed.html', {'listing':listing, 'photos':photos})

@login_required
def delete(request, listing_id):
	listing = get_object_or_404(Listing, id=listing_id)
	if request.user == listing.user:
		listing.delete()
		return redirect('listings.views.dashboard')

# from django.core.context_processors import csrf
def search(request):
	#c = {}
	#c.update(csrf(request))
	return TemplateResponse("listings/search_test.html")

@require_POST
def search_ajax(request):
	search_text = request.POST.get('search_text', '').strip()

	if search_text:
		listings = SearchQuerySet().autocomplete(content_auto=search_text)
	else:
		listings = SearchQuerySet().all()

	for listing in listings:
		listing.url_id = reverse(listing) # 'listings.views.detail', args=[str(listing.url_id)])

	return TemplateResponse(request, 'listings/partials/ajax_search.html', {'listings' : listings})

# Photo upload

# if not settings.DEBUG:
# 	upload_backend = ProductionUploadBackend
# else:
# 	upload_backend = DevelopmentUploadBackend


# import_uploader = AjaxFileUploader(backend=upload_backend)

def status(request, listing_id):
	listing = get_object_or_404(Listing, id=listing_id)
	return HttpResponse(listing.status)
