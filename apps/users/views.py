from listings.models import Listing, ListingPhoto, Buyer, Offer, Message
import datetime
#from users.models import UserProfile
from users.forms import UserProfileForm, CommentSubmitForm
from users.models import UserProfile
from users.models import UserComment
from django.forms.models import inlineformset_factory
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
	commentForm = CommentSubmitForm(initial={'date_posted':datetime.datetime.now(),'user':user})
	listings = Listing.objects.filter(user=user).order_by('-pub_date')[:10]
	photos = ListingPhoto.objects.filter(listing=user)
	# provide `url` and `thumbnail_url` for convenience.
	photos = map(lambda photo: {'url':photo.url, 'order':photo.order}, photos)
	user_comments = UserComment.objects.filter(user=user)
	if request.method == 'POST':
		user_comment_form = CommentSubmitForm(request.POST, instance = user_comments)
		if user_comment_form.is_valid():
			# user_comment_form.name = form.cleaned_data['name']
			# user_comment_form.email = form.cleaned_data['email']
			# user_comment_form.comment = form.cleaned_data['comment']
			user_comment = user_comment_form.save()
			responseData = serializers.serialize("json", UserComment.objects.filter(user=user))
			return HttpResponse(responseData, content_type="application/json")
		else:
			errors = user_comment_form.errors
			return HttpResponse(simplejson.dumps(errors), content_type="application/json")
	else:
		return render(request, 'user_profile.html', {'user':user, 'listings':listings, 'photos':photos, 'user_comments':user_comments, 'CommentSubmitForm':commentForm})


# @login_required
# def edit(request, username):
# 	if request.user.username == username:
# 		user = request.user
# 		profile = user.get_profile()
# 		print "valid"
# 		if request.method == 'POST':
# 			user_profile_form = UserProfileForm(request.POST, instance = profile)
# 			print "post"
# 			if user_profile_form.is_valid():
# 				user_profile = user_profile_form.save()
# 				return redirect(user_profile)
# 				print "save"
# 			else:
# 				return render(request, 'user_edit.html', {'form': user_profile_form})
# 		else:
# 			return render(request, 'user_edit.html', {'form': UserProfileForm(instance = profile),})
# 	else:
# 		raise PermissionDenied

