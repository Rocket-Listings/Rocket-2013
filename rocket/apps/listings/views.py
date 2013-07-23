from listings.models import *
from listings import utils
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime, timedelta
from listings.forms import ListingForm, ListingPics, SpecForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST 
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import simplejson
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from rocket import get_client_ip
from django.db.models import Max
from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest
from operator import __add__ as combine
from django.http import Http404
from django.forms.models import inlineformset_factory

# @login_required
# def user_listings(request, username=None):
#   user = request.user # if no username parameter is passed, defaults to the currently logged in user.
#   if username:
#       user = get_object_or_404(User, username=username)
#   listings = Listing.objects.filter(user=user).order_by('-pub_date')[:10]
#   buyers = Buyer.objects.filter(listing__user=user)
#   messages = Message.objects.filter(listing__user=user)
#   return render(request, 'listings/dashboard.html', {'listings': listings, 'buyers': buyers, 'messages':messages,})

@login_required
def dashboard(request):
    user = request.user
    listings = Listing.objects.filter(user=user).order_by('-pub_date').all() # later on we can change how many are returned
    buyers = reduce(combine, map(lambda l: list(l.buyer_set.all()), listings), [])
    messages = reduce(combine, map(lambda b: list(b.message_set.all()), buyers), [])
    return render(request, 'listings/dashboard.html',  {'listings': listings, 'buyers': buyers, 'messages':messages})

@login_required
<<<<<<< HEAD
def create(request, pane='edit'):
    if request.method == 'GET':
        profile = request.user.get_profile()
        defaults = {
            'location': profile.location, 
            'category': profile.default_category, 
            'listing_type': profile.default_listing_type,
        }
        cxt = {
            'form': ListingForm(initial=defaults),
            'pane': pane
        }
        cxt.update(utils.get_listing_vars())
        return render(request, 'listings/detail.html', cxt)
    else: # POST
        return update(request)

@login_required
@require_POST
def update(request, listing_id=None): # not directly addressed by a route, allows DRY listing saving
    if listing_id:
        listing = get_object_or_404(Listing, id=listing_id)
        specs = listing.listingspecvalue_set.select_related()

        if request.user != listing.user:
            raise Http404
        # spec_form
        listing_form = ListingForm(request.POST, instance=listing)
        spec_form = SpecForm(request.POST, initial=specs) # SpecForm is not a real form
    else:
        listing_form = ListingForm(request.POST)
        spec_form = SpecForm(request.POST)

    if listing_form.is_valid() and spec_form.is_valid():

        listing = listing_form.save(commit=False)
        listing.user = request.user
        listing.save()
        for name, value in spec_form.cleaned_data.items():
            print name
            spec_id = int(name.replace('spec-',''))
            ListingSpecValue.objects.create(value=value, key_id=spec_id, listing_id=listing.id)
        return redirect(listing)
    else:
        # preserving validation errors
        cxt = {
            'form': listing_form,
            'spec_form': spec_form,
            'pane': 'edit',
        }
        cxt.update(utils.get_listing_vars())
        return render(request, 'listings/detail.html', cxt)

# detail is for the user looking at his own listing
def detail(request, listing_id, pane='view'):
    if request.method == 'GET':
        listing = get_object_or_404(Listing, id=listing_id)
        specs_set = listing.listingspecvalue_set.select_related().all()
        specs = {}
        for spec in specs_set:
            specs[spec.key.id] = spec
        cxt = {
            'listing': listing,
            'photos': listing.listingphoto_set.all(),
            'specs': specs,
        }
        if listing.user == request.user:
            form = ListingForm(instance=listing)
            spec_form = SpecForm(initial=specs)
            cxt.update(utils.get_listing_vars())
            cxt.update({
                'form': form,
                'pane': pane
            })
            return render(request, 'listings/detail.html', cxt)
        else:
            return render(request, 'listings/detail_public.html', cxt)
    else: # POST
        return update(request, listing_id)

def embed(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    photos = ListingPhoto.objects.filter(listing=listing).order_by('order')

    # provide `url` and `thumbnail_url` for convenience.
    photos = map(lambda photo: {'url':photo.url, 'order':photo.order}, photos)
    return render(request, 'listings/cl_embed.html', {'listing':listing, 'photos':photos})

@login_required
def delete(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.user == listing.user:
        listing.delete()
        return redirect('listings.views.dashboard')


# def delete_ajax(request, listing_id):
#   response = {}
#   try:
#       listing = Listing.objects.get(id=listing_id)
#   except ObjectDoesNotExist:
#       response['success'] = False
#       response['reason'] = 'Cannot find listing.'
#   if request.user == listing.user:
#       listing.delete()
#       response['success']= True
#   else:
#       response['success'] = False
#       response['reason'] = 'Cannot delete someone else\'s listings!'
#   return HttpResponse(simplejson.dumps(response), content_type = 'application/javascript; charset=utf8')

### DASHBOARD

#this is my first api so I'm not gonna join the requests. If this is too slow
#it wont be too hard to redo
# def listing_buyers_ajax(request, listing_id):
    # '''Returns a list of Buyers associated with the listing id (of the logged in user)'''
    # listing = get_object_or_404(Listing, id=listing_id)
    # buyers = listing.buyer_set.all().order_by('name')

    # for buyer in buyers:
    #   buyer.curMaxOffer =  buyer.max_offer()

    # if 'application/json' in request.META.get('HTTP_ACCEPT'):
    # json = serializers.serialize("json", buyers)
    # return HttpResponse(serializers.serialize("json", buyers), mimetype='application/json')
    # else:
        # return HttpResponseBadRequest("Sorry please submit a good request")

# def message_thread_ajax(request, listing_id, buyer_id):
#   listing = get_object_or_404(Listing, id=listing_id)
#   buyer = get_object_or_404(Buyer, id=buyer_id)
#   messages = listing.message_set.filter(buyer_id__exact=buyer_id).order_by('date')

    # if 'application/json' in request.META.get('HTTP_ACCEPT'):
    # return HttpResponse(serializers.serialize("json", messages), mimetype='application/json')
    # else:
        # return HttpResponseBadRequest("Sorry please submit a good request")
