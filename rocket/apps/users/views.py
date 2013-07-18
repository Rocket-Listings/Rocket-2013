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
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseForbidden
from django.utils import simplejson as json
from django.conf import settings
from twython import Twython

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
			return HttpResponse(json.dumps(errors), content_type="application/json")
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

@login_required
def obtain_twitter_auth_url(request):
	twitter = Twython(settings.TWITTER_KEY, settings.TWITTER_SECRET)
	auth = twitter.get_authentication_tokens(callback_url='http://local.rocketlistings.com:8000/users/twitter/callback')
	request.session['OAUTH_TOKEN'] = auth['oauth_token']
	request.session['OAUTH_TOKEN_SECRET'] = auth['oauth_token_secret']
	return HttpResponseRedirect(auth['auth_url'])

@login_required
def verify_twitter(request):
	if request.GET.get("oauth_verifier"):
		user = request.user
		oauth_verifier = request.GET.get('oauth_verifier', "")
		_OAUTH_TOKEN = request.session.get('OAUTH_TOKEN') #handshake token
		_OAUTH_TOKEN_SECRET = request.session.get('OAUTH_TOKEN_SECRET') #handshake secret
		_twitter = Twython(settings.TWITTER_KEY, settings.TWITTER_SECRET, _OAUTH_TOKEN, _OAUTH_TOKEN_SECRET)
		twitter_auth_keys = _twitter.get_authorized_tokens(oauth_verifier)
		
		UserProfile.objects.filter(user=user).update(OAUTH_TOKEN=twitter_auth_keys['oauth_token']) #real token
		UserProfile.objects.filter(user=user).update(OAUTH_TOKEN_SECRET=twitter_auth_keys['oauth_token_secret']) #real secret

		return redirect('/users/twitter/close')
	elif request.GET.get("denied"):
		return redirect('/users/twitter/close')
	else:
		return HttpResponseForbidden()

@login_required
def get_twitter_handle(request):
	if request.is_ajax():
		OAUTH_TOKEN = UserProfile.objects.filter(user=request.user).values("OAUTH_TOKEN")[0]['OAUTH_TOKEN']
		OAUTH_TOKEN_SECRET = UserProfile.objects.filter(user=request.user).values("OAUTH_TOKEN_SECRET")[0]['OAUTH_TOKEN_SECRET']
		twitter = Twython(settings.TWITTER_KEY, settings.TWITTER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
		handle = twitter.verify_credentials()['screen_name']
		UserProfile.objects.filter(user=request.user).update(twitter_handle=handle)
		return HttpResponse(json.dumps(handle), content_type='application/json')
	else:
		return HttpResponseForbidden()

def disconnect_twitter(request):
	if request.is_ajax():
		UserProfile.objects.filter(user=request.user).update(OAUTH_TOKEN="")
		UserProfile.objects.filter(user=request.user).update(OAUTH_TOKEN_SECRET="")
		UserProfile.objects.filter(user=request.user).update(twitter_handle="")
		return HttpResponse(json.dumps("success"), content_type='application/json')
	else:
		return redirect('/users/login')

@login_required
def twitter_connected(request):
	if request.is_ajax():
		if UserProfile.objects.filter(user=request.user).values("twitter_handle")[0]['twitter_handle'] != "":
			response = True
		else:
			response = False
		return HttpResponse(json.dumps(response), content_type='application/json')
	else:
		return HttpResponseForbidden()

@login_required
def have_oauth(request):
	if request.is_ajax():
		if UserProfile.objects.filter(user=request.user).values("OAUTH_TOKEN")[0]['OAUTH_TOKEN'] != "":
			response = True
		else:
			response = False
		return HttpResponse(json.dumps(response), content_type='application/json')
	else:
		return HttpResponseForbidden()
