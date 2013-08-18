from listings.models import *
from listings import utils
import json
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime, timedelta
from listings.forms import ListingForm, SpecForm, ListingPhotoFormSet, MessageForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST 
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import simplejson, formats
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
import haystack
from users.decorators import first_visit, view_count
from django.template.response import TemplateResponse
from django.contrib.humanize.templatetags.humanize import naturaltime
from mail.tasks import send_message_task
from users.models import UserProfile, UserComment 
from django.db.models import Avg
from listings.tasks import cl_anon_autopost_task, cl_anon_update_task, cl_delete_task

@first_visit
@login_required
def dashboard(request):
	listings = Listing.objects.filter(user=request.user).order_by('-pub_date').all() # later on we can change how many are returned
	buyers = reduce(combine, map(lambda l: list(l.buyer_set.all()), listings), [])
	messages = reduce(combine, map(lambda b: list(b.message_set.all()), buyers), [])
	latest_ids = map(lambda set: map(lambda i: i.id, set), [listings, buyers, messages])
	for i, val in enumerate(latest_ids):
		try:
			latest_ids[i] = max(val)
		except ValueError:
			latest_ids[i] = 0
	return TemplateResponse(request, 'listings/dashboard.html',  {'listings': listings, 
																	'buyers': buyers, 
																	'buyer_messages':messages, 
																	'latest': latest_ids})

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
			'listing_type': profile.seller_type,
		}
		cxt = {
			'form': ListingForm(initial=defaults),
			'pane': pane,
			'photo_formset': ListingPhotoFormSet(prefix="listingphoto_set")
		}
		cxt.update(utils.get_listing_vars())
		return TemplateResponse(request, 'listings/detail.html', cxt)
	else: # POST
		return update(request, create=True)

@login_required
@require_POST
def update(request, listing_id=None, create=False): # not directly addressed by a route, allows DRY listing saving
	if listing_id:
		listing = get_object_or_404(Listing, id=listing_id)
		if request.user != listing.user:
			raise Http404
	else:
		listing = Listing()

	listing_form = ListingForm(request.POST, instance=listing)
	specs = listing.listingspecvalue_set.select_related()
	spec_form = SpecForm(request.POST, initial=specs)
	photo_formset = ListingPhotoFormSet(request.POST, instance=listing, prefix="listingphoto_set")

	if listing_form.is_valid() and spec_form.is_valid() and photo_formset.is_valid():
		listing = listing_form.save(commit=False)
		listing.user = request.user
		listing.save()	
		# update search index
		haystack.connections['default'].get_unified_index().get_index(Listing).update_object(listing)

		for name, value in spec_form.cleaned_data.items():
			if value:
				spec_id = int(name.replace('spec-',''))
				ListingSpecValue.objects.create(value=value, key_id=spec_id, listing_id=listing.id)

		# for form in photo_formset.marked_for_delete:
			# form.instance.delete()

		photo_formset.save(commit=False)
		for form in photo_formset.ordered_forms:
			form.instance.order = form.cleaned_data['ORDER']
			form.instance.save()

		if listing.listing_type == "O":
			cl_type = "fso"
			cl_cat = str(listing.category.cl_owner_id)
		else: # Dealer
			cl_type = "fsd"
			cl_cat = str(listing.category.cl_dealer_id)

		autopost_cxt = {'type': cl_type,
			'cat': cl_cat,
			'title': listing.title,
			'price': str(listing.price),
			'location': listing.location,
			'description': listing.description,
			'from': listing.user.username + "@" + settings.MAILGUN_SERVER_NAME,
			'photos': map(lambda p: settings.S3_URL + p.key, listing.listingphoto_set.all()),
			'pk': listing.pk
		}

		if create:
			request.user.get_profile().subtract_credit()
			if not settings.AUTOPOST_DEBUG:
				cl_anon_autopost_task.delay(autopost_cxt)
		else: # Update
			if not settings.AUTOPOST_DEBUG:
				autopost_cxt['update_url'] = listing.CL_link
				cl_anon_update_task.delay(autopost_cxt)
		return redirect(listing)
	else:
		print listing_form.errors
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
	listing = get_object_or_404(Listing.objects.select_related(), id=listing_id)
	is_owner = bool(listing.user == request.user)
	request.user.is_owner = is_owner

	# prep specs
	specs_set = listing.listingspecvalue_set.select_related().all()
	specs = {}
	for spec in specs_set:
		specs[spec.key_id] = spec

	if request.method == 'GET':
		if is_owner:
			form = ListingForm(instance=listing)
			photo_formset = ListingPhotoFormSet(instance=listing, prefix="listingphoto_set")

			cxt = {
				'form': form,
				'specs': specs,
				'photo_formset': photo_formset,
				'pane': pane
			}
			cxt.update(utils.get_listing_vars())
			return TemplateResponse(request, 'listings/detail.html', cxt)
		else:
			comments = UserComment.objects.filter(user=listing.user).order_by('-date_posted') 
			avg_rating = comments.aggregate(Avg('rating')).values()[0]

			fbProfile = user.get_profile().fbProfile
			photos = listing.listingphoto_set.all()
			cxt = {
				'listing': listing,
				'photos': photos,
				'specs': specs,
				'fb' : fbProfile, 
				'avg_rating' : avg_rating 
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

def delete(request, listing_id):
	listing = get_object_or_404(Listing, id=listing_id)
	if request.user == listing.user:
		# remove listing from haystack index
		haystack.connections['default'].get_unified_index().get_index(Listing).remove_object(listing)
		cl_cxt = {'update_url': listing.CL_link, 'pk': listing.pk}
		if not settings.AUTOPOST_DEBUG:
			cl_delete_task.delay(cl_cxt)
		listing.delete()
		return HttpResponse(200)
	else:
		return HttpResponse(403)

@require_GET
def search(request):
	search_text = request.GET.get('search', '')
	listings = SearchQuerySet().filter(content=search_text)[:20]	
	cxt = { 'listings': listings }
	return TemplateResponse(request, "listings/search.html", cxt)

def search_ajax(request):
	search_text = request.REQUEST.get('search', '').strip()
	listings = SearchQuerySet().filter(content=search_text)[:20]
	cxt = { 'listings': listings }
	# for listing in listings:
		# listing.url_id = reverse('listings.views.detail', args=[str(listing.url_id)])
	return TemplateResponse(request, 'listings/partials/ajax_search.html', cxt)

# Photo upload

# if not settings.DEBUG:
# 	upload_backend = ProductionUploadBackend
# else:
# 	upload_backend = DevelopmentUploadBackend


# import_uploader = AjaxFileUploader(backend=upload_backend)

### API ###
@require_GET
def status(request, listing_id):
	listing = get_object_or_404(Listing, id=listing_id)
	return HttpResponse(listing.status)

@require_GET
def update_status(request, listing_id):
	listing = get_object_or_404(Listing, id=listing_id)
	if request.user == listing.user:
		new_status = request.GET.get('status', '')
		status_dict = {'Draft': 1, 'Pending': 2, 'Active': 3, 'Sold': 4, 'Deleted': 5}
		if new_status in status_dict:
			listing.status_id = status_dict[new_status]
			listing.save()
			response_dict = {'id': listing.id, 'status': listing.status.name}
			return HttpResponse(simplejson.dumps({'listing': response_dict, 'status': 'success'}), content_type='application/json')
		else:
			return HttpResponse(simplejson.dumps({'listing': listing.id, 'status': 'status error'}), content_type='application/json')
	else:
		return HttpResponse(403)


@require_GET
def dashboard_data(request):
	user = request.user
	ids = map(lambda i: int(request.GET.get(i, '0')), ['listing', 'buyer', 'message'])

	listings = Listing.objects.filter(user=user).order_by('-pub_date').all()
	buyers = reduce(combine, map(lambda l: list(l.buyer_set.all()), listings), [])
	messages = reduce(combine, map(lambda b: list(b.message_set.all()), buyers), [])
	latest_ids = map(lambda set: map(lambda i: i.id, set), [listings, buyers, messages])
	for i, val in enumerate(latest_ids):
		try:
			latest_ids[i] = max(val)
		except ValueError:
			latest_ids[i] = 0

	listings_data = map(lambda l: {
		'title': l.title, 
		'link': l.get_absolute_url(), 
		'id': l.id, 
		'price': l.price, 
		'category': l.category.name, 
		'status': l.status.name,
		'status_lower': l.status.name.lower(),
		'sort_date': l.pub_date.strftime("%m/%d/%y %I:%M %p"),
		'natural_date': naturaltime(l.pub_date)}, listings.filter(id__gt=ids[0]))
	buyers_data = map(lambda b: {
		'listing_id': b.listing.id, 
		'buyer_id': b.id, 
		'max_offer': b.curMaxOffer, 
		'name': b.name, 
		'last_message_date': naturaltime(b.last_message().date)}, [b for b in reversed(buyers) if b.id > ids[1]])
	messages_data = map(lambda m: {
		'isSeller': m.isSeller,
		'buyer_id': m.buyer.id,
		'buyer_name': m.buyer.name,
		'seller_name': m.listing.user.get_profile().get_display_name(),
		'listing_id': m.listing.id,
		'message_id': m.id,
		'content': m.content,
		'date': naturaltime(m.date)}, [m for m in messages if m.id > ids[2]])

	json = {'listings': listings_data, 'buyers': buyers_data, 'messages': messages_data, 'latest': latest_ids}
	return HttpResponse(simplejson.dumps(json), content_type="application/json")

@require_POST
def dashboard_message(request):
	if request.POST.get("content", ""):
		message_form = MessageForm(request.POST)
		if message_form.is_valid():
			message = message_form.save(commit=False)
			message.isSeller = True
			message.save()
			send_message_task.delay(message.id)
			response_data = { 'listing_id': message.listing.id,
							  'isSeller': message.isSeller,
							  'seller_name': message.listing.user.get_profile().get_display_name(),
							  'buyer_id': message.buyer.id,
							  'buyer_name': message.buyer.name,
							  'content': message.content,
							  'message_id': message.id,
							  'date': naturaltime(message.date) }
			return HttpResponse(simplejson.dumps({'messages': response_data, 'status': 'success'}), content_type="application/json")
		else:
			return HttpResponse(simplejson.dumps({'errors': message_form.errors, 'status': 'err_validation'}), content_type="application/json")
	else:
		return HttpResponse(simplejson.dumps({'errors': 'Message content is empty.', 'status': 'err_empty'}))

@require_GET
@login_required
def message_seen(request):
	message = get_object_or_404(Message, id=request.GET.get("message_id", ""))
	if request.user == message.listing.user:
		message.seen = True
		message.save()
		msg_dict = {'message_id': message.id,
					'buyer_id': message.buyer.id,
					'listing_id': message.listing.id,
					'listing_all_read': all(map(lambda m: m.seen, message.listing.message_set.all()))}
		return HttpResponse(simplejson.dumps({'message_data': msg_dict, 'status': 'success'}), content_type="application/json")
	else:
		return HttpResponse(simplejson.dumps({'status': 'Error: This action is forbidden.'}), content_type="application/json")

