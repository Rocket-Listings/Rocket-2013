from listings.models import Listing, ListingPhoto, Buyer, Offer, Message, ListingStatus
import datetime
#from users.models import UserProfile
from users.forms import UserProfileForm, CommentSubmitForm
from users.models import UserProfile, UserComment
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
#from forms import UserProfileForm
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.core import serializers
from django.http import HttpResponse, HttpRequest
from django.utils import simplejson as json

def overview(request, username=None):
	return info(request, username)

@login_required
def info(request):
	user = request.user
	profile = user.get_profile()
	if request.method == 'POST':
		user_profile_form = UserProfileForm(request.POST, instance=profile)
		if user_profile_form.is_valid():	
			User.objects.filter(username = user).update(email=user_profile_form.cleaned_data['email'])
			user_profile = user_profile_form.save()
			responseData = {}
			for key, value in user_profile_form.cleaned_data.iteritems():
				responseData[key] = value
			responseData['profile'] = True		
			return HttpResponse(json.dumps(responseData), content_type="application/json")
		else:
			errors = user_profile_form.errors
			return HttpResponse(json.dumps(errors), content_type="application/json")
	else:
		return render(request, 'users/user_info.html', {'user': user})


def profile(request, username=None):
	user = User.objects.get(username=username)
	allListings = Listing.objects.filter(user=user).order_by('-pub_date')
	activelistings = allListings.filter(status=ListingStatus(pk=1))
	draftlistings = allListings.filter(status=ListingStatus(pk=2))
	photos = ListingPhoto.objects.filter(listing=user)
	photos = map(lambda photo: {'url':photo.url, 'order':photo.order}, photos)
	comments = UserComment.objects.filter(user=user).order_by('-date_posted')[:5]
	if request.method == 'POST':
		comment_form = CommentSubmitForm(request.POST, instance = UserComment(user=user))
		if comment_form.is_valid():
			comment = comment_form.save()
			responseData = serializers.serialize("json", UserComment.objects.filter(pk=comment.pk));
			return HttpResponse(responseData, content_type="application/json")
		else:
			errors = comment_form.errors
			return HttpResponse(simplejson.dumps(errors), content_type="application/json")
	else:
		return render(request, 'users/user_profile.html', {'user':user, 'activelistings':activelistings, 'draftlistings':draftlistings, 'photos':photos, 'comments':comments})

def delete_account(request):
	user = request.user
	if user.is_authenticated():
		user_to_delete = User.objects.get(username=user)
		user_to_delete.delete()
		return redirect('/')
	else:
		return redirect('/users/login')