from listings.models import Listing, ListingPhoto, Buyer, Offer, Message 
#from users.models import UserProfile
from users.forms import UserProfileForm
from users.models import UserProfile
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
#from forms import UserProfileForm
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.core import serializers
from django.http import HttpResponse, HttpRequest
from django.utils import simplejson

def overview(request, username=None):
	return info(request, username)

@login_required
def info(request):
	user = request.user
	profile = user.get_profile()
	if request.method == 'POST':
		user_profile_form = UserProfileForm(request.POST, instance=profile)
		if user_profile_form.is_valid():
			user_profile = user_profile_form.save()
			User.objects.filter(username = user).update(email=request.POST['email'])
			responseData = serializers.serialize("json", UserProfile.objects.filter(user=user))
			return HttpResponse(responseData, content_type="application/json")
		else:
			errors = user_profile_form.errors
			return HttpResponse(simplejson.dumps(errors), content_type="application/json")
	else:
		return render(request, 'user_info.html', {'user': user})

def profile(request, username=None):
	user = User.objects.get(username=username)
	listings = Listing.objects.filter(user=user).order_by('-pub_date')[:10]
	photos = ListingPhoto.objects.filter(listing=user)
	# provide `url` and `thumbnail_url` for convenience.
	photos = map(lambda photo: {'url':photo.url, 'order':photo.order}, photos)
	return render(request, 'user_profile.html', {'user':user, 'listings':listings, 'photos':photos})
