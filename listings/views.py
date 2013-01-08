from listings.models import Listing, ListingPhoto
from django.conf import settings
from datetime import datetime, timedelta
from listings.forms import ListingForm
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from ajaxuploader.views import AjaxFileUploader
from ListingsLocalUploadBackend import ListingsLocalUploadBackend

def latest(request):
	listings = Listing.objects.all().order_by('-pub_date')[:10]
	return render(request, 'listings_latest.html', {'listings': listings,})


def create(request):
	if request.method == 'GET':
		return render(request, 'listing_create.html', {'form':ListingForm(),})
	elif request.method == 'POST':
		listing_form = ListingForm(request.POST)
		if listing_form.is_valid():
			listing = listing_form.save(commit=False)
			listing.user = request.user
			listing.save()
			expire_time = datetime.now() - timedelta(minutes=settings.ROCKET_UNUSED_PHOTO_MINS)
			ListingPhoto.objects.filter(ip=request.META['REMOTE_ADDR'], upload_date__gt=expire_time).update(listing=listing)
			if request.user.is_authenticated():

				return redirect(listing)
			else:
				return redirect(listing)
				# Do something for anonymous users.
		else:
			return render(request, 'listing_create.html', {'form': ListingForm(request.POST),})


def detail(request, listing_id):
	listing = Listing.objects.get(id__exact = listing_id)
	return render(request, 'listing_detail.html', {'listing':listing,})


@login_required
def update(request, listing_id):
	listing = Listing.objects.get(id__exact = listing_id)
	if request.user == listing.user: # updating his own listing
		if request.method == 'POST':
			listing_form = ListingForm(request.POST, instance = listing)		
			if listing_form.is_valid():
				listing = listing_form.save()
				return redirect(listing)
			else:
				return render(request, 'listing_update.html', {'form': listing_form})
		else:
			return render(request, 'listing_update.html', {'form':ListingForm(instance = listing),}, context_instance = RequestContext(request))
	else:
		return render(request, '403.html')


@login_required
def delete(request, listing_id):
	listing = Listing.objects.get(id__exact = listing_id)
	if request.user == listing.user:
		listing.delete()
		return redirect('account_overview')

import_uploader = AjaxFileUploader(backend=ListingsLocalUploadBackend)