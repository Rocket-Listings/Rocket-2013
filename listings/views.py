from listings.models import Listing, ListingPhoto
from django.conf import settings
from datetime import datetime, timedelta
from listings.forms import ListingForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ajaxuploader.views import AjaxFileUploader
from ListingsLocalUploadBackend import ListingsLocalUploadBackend
from django.utils import simplejson
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
def latest(request):
	listings = Listing.objects.all().order_by('-pub_date')[:10]
	return render(request, 'listings_latest.html', {'listings': listings,})

@login_required
def create(request):
	if request.method == 'GET':
		profile = request.user.profile
		defaults = {'location':profile.location, 'category':profile.default_category, 'listing_type':profile.default_listing_type}
		form = ListingForm(initial=defaults)
		return render(request, 'listing_create.html', {'form':form})
	elif request.method == 'POST':
		listing_form = ListingForm(request.POST)
		if listing_form.is_valid():
			listing = listing_form.save(commit=False)
			listing.user = request.user
			listing.save()
			expire_time = datetime.now() - timedelta(minutes=settings.ROCKET_UNUSED_PHOTO_MINS)
			ListingPhoto.objects.filter(upload_ip=request.META['REMOTE_ADDR'], upload_date__gt=expire_time).update(listing=listing)
			if request.user.is_authenticated():
				return redirect(listing)
			else:
				return redirect(listing)
				# Do something for anonymous users.
		else:
			return render(request, 'listing_create.html', {'form': ListingForm(request.POST),})


def detail(request, listing_id):
	listing = get_object_or_404(Listing, id=listing_id)
	photos = ListingPhoto.objects.filter(listing=listing).order_by('order')

	# provide `url` and `thumbnail_url` for convenience.
	photos = map(lambda photo: {'url':photo.url, 'order':photo.order}, photos) 
	return render(request, 'listing_detail.html', {'listing':listing, 'photos':photos})

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
		return redirect('users.views.overview')

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

import_uploader = AjaxFileUploader(backend=ListingsLocalUploadBackend)