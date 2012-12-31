from listings.models import Listing
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404 #, redirect
from django.contrib.auth.decorators import login_required

#def login(request):
#	return render(request, 'login.html', {'form': AuthenticationForm() }, context_instance=RequestContext(request))

#def logout(request):
	# Redirect to a success page.

@login_required
def overview(request, username=None):
	user = request.user # if no username parameter is passed, defaults to the currently logged in user.
	if username:
		user = get_object_or_404(User, username=username)
	listings = Listing.objects.filter(user=user).order_by('pub_date')
	return render(request, 'account_overview.html', {'listings': listings})

	
@login_required
def listings(request, username):
	user = request.user # if no username parameter is passed, defaults to the currently logged in user.
	if username:
		user = get_object_or_404(User, username=username)
	listings = Listing.objects.filter(user=user).order_by('pub_date')
	return render(request, 'account_overview.html', {'listings': listings})

@login_required
def info(request, username):
	return None