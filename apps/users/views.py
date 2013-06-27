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
from django.http import HttpResponse

def overview(request, username=None):
	return info(request, username)

@login_required
def info(request, username=None):
	if request.user.username == username:
		user = request.user
		profile = user.get_profile()
		if request.method == 'POST':
			user_profile_form = UserProfileForm(request.POST, instance = profile)
			print request.POST
			if user_profile_form.is_valid():
				user_profile = user_profile_form.save()
				responseData = serializers.serialize("json", UserProfile.objects.filter(user=user))
				print responseData
				return HttpResponse(responseData, content_type="application/json")
			else:
				responseData = serializers.serialize("json", UserProfile.objects.filter(user=user))
				return HttpResponse(responseData, content_type="application/json")
		else:
			return render(request, 'user_info.html', {'profile': profile})
	else:
		raise PermissionDenied

	# profile = request.user.get_profile()
	# return render(request, 'user_info.html', {'profile':profile,})

@login_required
def profile(request, username=None):
	print username
	profile = request.user.get_profile()
	relevant_user = request.user
	user=relevant_user
	listings = Listing.objects.filter(user=relevant_user).order_by('-pub_date')[:10]
	photos = ListingPhoto.objects.filter(listing=relevant_user)
	# provide `url` and `thumbnail_url` for convenience.
	photos = map(lambda photo: {'url':photo.url, 'order':photo.order}, photos) 
	return render(request, 'user_profile.html', {'profile':profile, 'listings':listings, 'photos':photos, 'user':relevant_user})

@login_required
def edit(request, username):
	if request.user.username == username:
		user = request.user
		profile = user.get_profile()
		print "valid"
		if request.method == 'POST':
			user_profile_form = UserProfileForm(request.POST, instance = profile)
			print "post"
			if user_profile_form.is_valid():
				user_profile = user_profile_form.save()
				return redirect(user_profile)
				print "save"
			else:
				return render(request, 'user_edit.html', {'form': user_profile_form})
		else:
			return render(request, 'user_edit.html', {'form': UserProfileForm(instance = profile),})
	else:
		raise PermissionDenied
