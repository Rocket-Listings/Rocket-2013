from listings.models import Listing, ListingPhoto, Buyer, Offer, Message, ListingStatus
import datetime
#from users.models import UserProfile
from django.views.decorators.http import require_GET, require_POST
from users.forms import UserProfileForm, CommentSubmitForm
from users.models import UserProfile, UserComment 
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

@first_visit
@login_required
def info(request):
    user = request.user
    profile = user.get_profile()
    if request.method == 'GET':
        fbProfile = profile.fbProfile
        view_count = get_view_count(request.user)

        credits = profile.listing_credits
        credits_spent = profile.total_credits - credits

        profile_completed_once = profile.profile_completed_once
        twitter_connected_once = profile.twitter_connected_once
        facebook_connected_once = profile.facebook_connected_once

        user_profile_form = UserProfileForm(instance=profile)
        cxt = {
            'user': user, 
            'form': user_profile_form, 
            'fb': fbProfile, 
            'credits':credits, 
            'credits_spent':credits_spent,
            'view_count': view_count,
            'profile_completed_once':profile_completed_once,
            'twitter_connected_once':twitter_connected_once, 
            'facebook_connected_once':facebook_connected_once
        }
        return TemplateResponse(request, 'users/info.html', cxt)
    else: # POST request
        user_profile_form = UserProfileForm(request.POST, instance=profile)
        if user_profile_form.is_valid():
            userObject = User.objects.get(username=user)
            userObject.email = user_profile_form.cleaned_data['email']
            userObject.save()
            responseData = {}
            for key, value in user_profile_form.cleaned_data.iteritems():
                if key != "default_listing_type" and key != "default_category":
                    responseData[key] = escape(value)
            responseData['profile'] = True
            responseData['credits_added'] = 0

            if profile.filled_out() and not profile.profile_completed_once:
                profile.profile_completed_once = True
                profile.add_credit(2)
                responseData['credits_added'] = 2
                responseData['profile_completed'] = True

            user_profile = user_profile_form.save() 

            return HttpResponse(json.dumps(responseData), content_type="application/json")
        else:
            errors = user_profile_form.errors
            return HttpResponse(json.dumps(errors), content_type="application/json")


@view_count
@first_visit
def profile(request, username=None):
    user = get_object_or_404(User, username=username)
    request.user.is_owner = bool(user == request.user) # put in to make the annotations work
    listings = Listing.objects.filter(user=user).order_by('-create_date')
    # activelistings = allListings.filter(status=ListingStatus(pk=1))
    # draftlistings = allListings.filter(status=ListingStatus(pk=2))
    #photos = ListingPhoto.objects.filter(listing=user)
    #photos = map(lambda photo: {'url':photo.url, 'order':photo.order}, photos)
    #ratings = UserRating.objects.filter(user=user)
    comments = UserComment.objects.filter(user=user).order_by('-date_posted') 
    avg_rating = comments.aggregate(Avg('rating')).values()[0]
    fbProfile = user.get_profile().fbProfile
    
    total_listing_views = sum(map(get_view_count, listings))

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
        #   comment = comment_form.save()
        #   responseData = serializers.serialize("json", UserComment.objects.filter(pk=comment.pk));
        #   return HttpResponse(responseData, content_type="application/json")
        # else:
        #   errors = comment_form.errors
        #   return HttpResponse(json.dumps(errors), content_type="application/json")
    else:
        credits = user.get_profile().listing_credits
        context_dictionary = {'url_user':user, 'listings': listings, 'comments':comments, 'fb': fbProfile, 'avg_rating':avg_rating, 'owner':request.user.is_owner, 'credits':credits,'total_listing_views':total_listing_views}
        return TemplateResponse(request, 'users/profile.html', context_dictionary) #'activelistings':activelistings, 'draftlistings':draftlistings,

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
            credits = 0
            response = {}
            response['handle'] = handle

            if not profile.twitter_connected_once:
                credits = 2
                profile.twitter_connected_once = True
                profile.add_credit(credits)

            response['credits_added'] = credits
            profile.save()

            return HttpResponse(json.dumps(response), content_type='application/json')
        else:
            response = {}
            response['handle'] = "no_oauth_token_or_key"
            return HttpResponse(json.dumps(response), content_type='application/json')
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
        if request.user.get_profile().twitter_handle != "":
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
@require_POST
def fb_profile(request):
    if request.is_ajax():
        fb = request.user.get_profile().fbProfile
        fb.username = request.POST.get('username', "")
        fb.name = request.POST.get('name', "")
        fb.link = request.POST.get('link', "")
        fb.picture = request.POST.get('picture', "")

        if fb.is_valid():
            fb.save()
            profile = request.user.get_profile()
            if not profile.facebook_connected_once:
                profile.facebook_connected_once = True
                profile.credits += 2
                profile.save()

            response = {
                'name': fb.name,
                'credits': profile.credits
            }
            return HttpResponse(json.dumps(response), content_type='application/json')
        else:
            return HttpResponseForbidden
    else:
        return HttpResponseForbidden

@login_required
def disconnect_fb(request):
    if request.is_ajax():
        request.get_profile().fbProfile.delete()
        return HttpResponse("success")
    else:
        return HttpResponseForbidden
