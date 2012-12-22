from listings.models import Listing
from listings.forms import ListingForm
from django.shortcuts import render_to_response, redirect
#from django.core.context_processors import csrf
from django.template import RequestContext

def latest(request):
	listings = Listing.objects.all().order_by('-pub_date')[:10]
	return render_to_response('latest.html', {'listings': listings,})

def create(request):
	#if request.user.is_authenticated():
    	# Do something for authenticated users.
	#else:
	    # Do something for anonymous users.
	if request.method == 'POST':
		listing_form = ListingForm(request.POST)
		if listing_form.is_valid():
			listing = listing_form.save()
			return redirect('latest-listings')
		else:
			return render_to_response('create.html', {'form': ListingForm(request.POST),})
	else:
		return render_to_response('create.html', {'form':ListingForm(),}, context_instance=RequestContext(request))


def read(request, listing_id):
	return render_to_response('read.html')