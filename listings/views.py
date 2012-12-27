from listings.models import Listing
from listings.forms import ListingForm
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.models import User

def latest(request):
	listings = Listing.objects.all().order_by('-pub_date')[:10]
	return render_to_response('latest.html', {'listings': listings,})


@login_required
def create(request):
	#if request.user.is_authenticated():
    	# Do something for authenticated users.
	#else:
	    # Do something for anonymous users.
	if request.method == 'POST':
		listing_form = ListingForm(request.POST)
		if listing_form.is_valid():
			listing = listing_form.save(commit=False)
			listing.user = request.user
			listing.save()
			return redirect(listing)
		else:
			return render_to_response('listing_create.html', {'form': ListingForm(request.POST),})
	else:
		return render_to_response('listing_create.html', {'form':ListingForm(),}, context_instance=RequestContext(request))


def read(request, listing_id):
	listing = Listing.objects.get(id__exact = listing_id)
	return render_to_response('listing_read.html', {'listing':listing,})


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
				return render_to_response('listing_update.html', {'form': listing_form})
		else:
			return render_to_response('listing_update.html', {'form':ListingForm(instance = listing),}, context_instance = RequestContext(request))
	else:
		return render_to_response('403.html')


@login_required
def delete(request, listing_id):
	listing = Listing.objects.get(id__exact = listing_id)
	if request.user == listing.user:
		listing.delete()
		return redirect('account_overview')