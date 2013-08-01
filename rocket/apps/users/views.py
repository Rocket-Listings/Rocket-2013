from listings.models import Listing, ListingPhoto, Buyer, Offer, Message, ListingStatus
import datetime
#from users.models import UserProfile
from users.forms import UserProfileForm, CommentSubmitForm
from users.models import UserProfile, UserComment, ProfileFB 
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
#from forms import UserProfileForm
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.mail import send_mail
from django.core import serializers
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseForbidden
from django.utils import simplejson as json
from django.conf import settings
from twython import Twython
from users.decorators import first_visit
from django.db.models import Avg
from users.decorators import first_visit, view_count
from utils import get_view_count
from cgi import escape


def overview(request, username=None):
	return info(request, username)

@first_visit
@login_required
def info(request):
	user = request.user
	profile = user.get_profile()
	fbProfile = ProfileFB.objects.get(profile=profile)
	if request.method == 'POST':
		user_profile_form = UserProfileForm(request.POST, instance=profile)
		print user_profile_form
		if user_profile_form.is_valid():
			userObject = User.objects.get(username=user)
			userObject.email = user_profile_form.cleaned_data['email']
			userObject.save()
			user_profile = user_profile_form.save()
			responseData = {}
			for key, value in user_profile_form.cleaned_data.iteritems():
				if key != "default_listing_type" and key != "default_category":
					responseData[key] = escape(value)
			responseData['profile'] = True
			return HttpResponse(json.dumps(responseData), content_type="application/json")
		else:
			errors = user_profile_form.errors
			return HttpResponse(json.dumps(errors), content_type="application/json")
	else:
		user_profile_form = UserProfileForm(instance=profile)
		return TemplateResponse(request, 'users/user_info.html', {'user': user, 'form': user_profile_form, 'fb': fbProfile})

@view_count
@first_visit
def profile(request, username=None):
	user = User.objects.get(username=username)
	
	if request.user.is_authenticated():
		request.user.skip_count = user.get_username() == request.user.get_username()
		
	allListings = Listing.objects.filter(user=user).order_by('-pub_date')
	# activelistings = allListings.filter(status=ListingStatus(pk=1))
	# draftlistings = allListings.filter(status=ListingStatus(pk=2))
	photos = ListingPhoto.objects.filter(listing=user)
	photos = map(lambda photo: {'url':photo.url, 'order':photo.order}, photos)
	#ratings = UserRating.objects.filter(user=user)
	#rating = ratings.aggregate(Avg('rating')).values()[0]
	comments = UserComment.objects.filter(user=user).order_by('-date_posted') 
	fbProfile = ProfileFB.objects.get(profile=user.get_profile())
	if request.method == 'POST':
		comment_form = CommentSubmitForm(request.POST, instance = UserComment(user=user))	
		if comment_form.is_valid():
			comment = comment_form.save()
			responseData = {}
			for key, value in comment_form.cleaned_data.iteritems():
				if isinstance(value, int):
					responseData[key] = escape(str(value))
				else:
					responseData[key] = escape(value)
			responseData['new_comment'] = True
			responseData['date_posted'] = datetime.date.today().strftime("%B %d, %Y")
			return HttpResponse(json.dumps(responseData), content_type="application/json")
		else:
			errors = comment_form.errors
			return HttpResponse(json.dumps(errors), content_type="application/json")


		# comment_form = CommentSubmitForm(request.POST, instance = UserComment(user=user))
		# if comment_form.is_valid():
		# 	comment = comment_form.save()
		# 	responseData = serializers.serialize("json", UserComment.objects.filter(pk=comment.pk));
		# 	return HttpResponse(responseData, content_type="application/json")
		# else:
		# 	errors = comment_form.errors
		# 	return HttpResponse(json.dumps(errors), content_type="application/json")
	else:
		return TemplateResponse(request, 'users/user_profile.html', {'url_user':user, 'listings':allListings, 'photos':photos, 'comments':comments, 'fb': fbProfile}) #'activelistings':activelistings, 'draftlistings':draftlistings,

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
		profile = UserProfile.objects.get(user=user)
		profile.TWITTER_OAUTH_TOKEN = twitter_auth_keys['oauth_token'] #real token
		profile.TWITTER_OAUTH_TOKEN_SECRET = twitter_auth_keys['oauth_token_secret'] #real secret
		try:
			profile.full_clean()
		except ValidationError:
			return HttpResponseForbidden()
		else:
			profile.save()
			return redirect('/users/twitter/close')
	elif request.GET.get("denied"):
		return redirect('/users/twitter/close')
	else:
		return HttpResponseForbidden()

@login_required
def get_twitter_handle(request):
	if request.is_ajax():
		TWITTER_OAUTH_TOKEN = UserProfile.objects.get(user=request.user).TWITTER_OAUTH_TOKEN
		TWITTER_OAUTH_TOKEN_SECRET = UserProfile.objects.get(user=request.user).TWITTER_OAUTH_TOKEN_SECRET
		if TWITTER_OAUTH_TOKEN != "":
			twitter = Twython(settings.TWITTER_KEY, settings.TWITTER_SECRET, TWITTER_OAUTH_TOKEN, TWITTER_OAUTH_TOKEN_SECRET)
			handle = twitter.verify_credentials()['screen_name']
			profile = UserProfile.objects.get(user=request.user)
			profile.twitter_handle = handle
			profile.save()
			return HttpResponse(json.dumps(handle), content_type='application/json')
		else:
			return HttpResponse(json.dumps("no_oauth_token_or_key"), content_type='application/json')
	else:
		return HttpResponseForbidden()

def disconnect_twitter(request):
	if request.is_ajax():
		profile = UserProfile.objects.get(user=request.user)
		profile.TWITTER_OAUTH_TOKEN = ""
		profile.TWITTER_OAUTH_TOKEN_SECRET = ""
		profile.twitter_handle = ""
		profile.save()
		return HttpResponse(json.dumps("success"), content_type='application/json')
	else:
		return redirect('/users/login')

@login_required
def twitter_connected(request):
	if request.is_ajax():
		if UserProfile.objects.get(user=request.user).twitter_handle != "":
			response = True
		else:
			response = False
		return HttpResponse(json.dumps(response), content_type='application/json')
	else:
		return HttpResponseForbidden()

@login_required
def have_oauth(request):
	if request.is_ajax():
		if UserProfile.objects.get(user=request.user).OAUTH_TOKEN != "":
			response = True
		else:
			response = False
		return HttpResponse(json.dumps(response), content_type='application/json')
	else:
		return HttpResponseForbidden()


@login_required
def fb_profile(request):
	if request.method == 'POST':
		if request.is_ajax():
			fb = ProfileFB.objects.get(profile=request.user)
			fb.username = request.POST.get('username', "")
			fb.name = request.POST.get('name', "")
			fb.link = request.POST.get('link', "")
			fb.picture = request.POST.get('picture', "")
			try:
				fb.full_clean()
			except ValidationError:
				return HttpResponseForbidden()
			else:
				fb.save()
				return HttpResponse(fb.name)
		else:
			return HttpResponseForbidden
	else:
		return HttpResponseForbidden

def disconnect_fb(request):
	if request.is_ajax():
		fb = ProfileFB.objects.get(profile=request.user)
		fb.username, fb.name, fb.link, fb.picture = "", "", "", ""
		fb.save()
		return HttpResponse("success")
	else:
		return redirect('/users/login')
