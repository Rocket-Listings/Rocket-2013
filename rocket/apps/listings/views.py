from listings.models import Listing, ListingPhoto, Spec, Message
from listings import utils
from django.conf import settings

import json
from django.contrib.auth.models import User

from datetime import datetime, timedelta
from listings.forms import ListingForm, SpecFormSet, ListingPhotoFormSet, MessageForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rocket import get_client_ip
from django.db.models import Max
from django.http import HttpResponse
from operator import __add__
from django.http import Http404
from django.core.urlresolvers import reverse
import haystack
from users.decorators import first_visit, view_count
from django.template.response import TemplateResponse
from django.contrib.humanize.templatetags.humanize import naturaltime
from mail.tasks import send_message_task
from users.models import UserProfile, UserComment 
from django.db.models import Avg
from listings.tasks import cl_anon_autopost_task, cl_anon_update_task, cl_delete_task

@first_visit
@login_required
def dashboard(request):
    listings = Listing.objects.filter(user=request.user).order_by('-create_date').all() # later on we can change how many are returned
    buyers = reduce(__add__, map(lambda l: list(l.buyer_set.all()), listings), [])
    messages = reduce(__add__, map(lambda b: list(b.message_set.all()), buyers), [])
    latest_ids = map(lambda set: map(lambda i: i.id, set), [listings, buyers, messages])
    for i, val in enumerate(latest_ids):
        try:
            latest_ids[i] = max(val)
        except ValueError:
            latest_ids[i] = 0
    context = {
        'listings': listings,
        'buyers': buyers,
        'buyer_messages':messages,
        'latest': latest_ids
    }
    return TemplateResponse(request, 'listings/dashboard.html', context)

@first_visit
@login_required
@require_GET
def create(request):
    profile = request.user.get_profile()
    listing = Listing.objects.create(user=request.user, category=profile.default_category, listing_type=profile.seller_type)
    return redirect('edit', listing.id)

@login_required
@require_POST
def update(request, listing_id=None, create=False): # not directly addressed by a route, allows DRY listing saving
	if listing_id:
		listing = get_object_or_404(Listing, id=listing_id)
		if request.user != listing.user:
			raise Http404
	else:
		listing = Listing()

	listing_form = ListingForm(request.POST, instance=listing, user=request.user)
	specs = listing.listingspecvalue_set.select_related()
	spec_form = SpecForm(request.POST, initial=specs)
	photo_formset = ListingPhotoFormSet(request.POST, instance=listing, prefix="listingphoto_set")

	if listing_form.is_valid() and spec_form.is_valid() and photo_formset.is_valid():
		listing = listing_form.save(commit=False)
		listing.user = request.user
		listing.save()	
		# update search index
		haystack.connections['default'].get_unified_index().get_index(Listing).update_object(listing)

		for name, value in spec_form.cleaned_data.items():
			if value:
				spec_id = int(name.replace('spec-',''))
				ListingSpecValue.objects.create(value=value, key_id=spec_id, listing_id=listing.id)

		# for form in photo_formset.marked_for_delete:
			# form.instance.delete()

		photo_formset.save(commit=False)
		for form in photo_formset.ordered_forms:
			form.instance.order = form.cleaned_data['ORDER']
			form.instance.save()
		if create:
			request.user.get_profile().subtract_credit()
			if not settings.AUTOPOST_DEBUG:			
				cl_anon_autopost_task.delay(listing.id)
		else: # Update
			if not settings.AUTOPOST_DEBUG:
				cl_anon_update_task.delay(listing.id)

		return redirect(listing)
	else:
		print listing_form.errors
		print photo_formset.errors
		# preserving validation errors
		cxt = {
			'form': listing_form,
			'spec_form': spec_form,
			'pane': 'edit',
			'photo_formset': photo_formset
		}
		cxt.update(utils.get_listing_vars())
		return TemplateResponse(request, 'listings/detail.html', cxt)

@view_count
@require_GET
def detail(request, listing_id, pane='preview'):
    listing = get_object_or_404(Listing.objects.select_related(), id=listing_id)
    photos = listing.listingphoto_set.all()
    specs = listing.spec_set.all()

    is_owner = bool(listing.user == request.user)
    request.user.is_owner = is_owner

    if is_owner:
        context = {
            'pane': pane,
            'listing': listing,
            'photos': photos,
            'specs': specs
        }
        context.update(utils.get_cats())
        return TemplateResponse(request, 'listings/detail.html', context)
    else: 
        comments = UserComment.objects.filter(user=listing.user).order_by('-date_posted') 
        avg_rating = comments.aggregate(Avg('rating')).values()[0]
        fbProfile = user.get_profile().fbProfile
        context = {
            'listing': listing,
            'photos': photos,
            'specs': specs,
            'fb' : fbProfile, 
            'avg_rating' : avg_rating 
        }
        return TemplateResponse(request, 'listings/detail_public.html', context)
        
        # =======
        #     # prep specs
        #     specs_set = listing.listingspecvalue_set.select_related().all()
        #     specs = {}
        #     for spec in specs_set:
        #         specs[spec.key_id] = spec

        #     if request.method == 'GET':
        #         if is_owner:
        #             form = ListingForm(instance=listing)
        #             photo_formset = ListingPhotoFormSet(instance=listing, prefix="listingphoto_set")

        #             cxt = {
        #                 'form': form,
        #                 'specs': specs,
        #                 'photo_formset': photo_formset,
        #                 'pane': pane
        #             }
        #             cxt.update(utils.get_listing_vars())
        #             return TemplateResponse(request, 'listings/detail.html', cxt)
        #         else:
        #             comments = UserComment.objects.filter(user=listing.user).order_by('-date_posted') 
        #             avg_rating = comments.aggregate(Avg('rating')).values()[0]

        #             fbProfile = user.get_profile().fbProfile
        #             photos = listing.listingphoto_set.all()
        #             cxt = {
        #                 'listing': listing,
        #                 'photos': photos,
        #                 'specs': specs,
        #                 'fb' : fbProfile, 
        #                 'avg_rating' : avg_rating 
        #             }
        #             return TemplateResponse(request, 'listings/detail_public.html', cxt)
        #     else: # POST
        #         return update(request, listing_id)

def delete(request, listing_id):
	listing = get_object_or_404(Listing, id=listing_id)
	if request.user == listing.user:
		# remove listing from haystack index
		haystack.connections['default'].get_unified_index().get_index(Listing).remove_object(listing)
		if not settings.AUTOPOST_DEBUG:
			cl_delete_task.delay(listing.id)
		return HttpResponse(200)
	else:
		return HttpResponse(403)

@require_GET
def search(request):
    search_text = request.GET.get('search', '')
    listings = SearchQuerySet().filter(content=search_text)[:20]    
    context = { 'listings': listings }
    return TemplateResponse(request, "listings/search.html", context)


# def embed(request, listing_id):
#     listing = get_object_or_404(Listing, id=listing_id)
#     photos = ListingPhoto.objects.filter(listing=listing).order_by('order')
#     # provide `url` and `thumbnail_url` for convenience.
#     photos = map(lambda photo: {'url':photo.url, 'order':photo.order}, photos)
#     return TemplateResponse(request, 'listings/cl_embed.html', {'listing':listing, 'photos':photos})

# @login_required
# def user_listings(request, username=None):
#   user = request.user # if no username parameter is passed, defaults to the currently logged in user.
#   if username:
#       user = get_object_or_404(User, username=username)
#   listings = Listing.objects.filter(user=user).order_by('-create_date')[:10]
#   buyers = Buyer.objects.filter(listing__user=user)
#   messages = Message.objects.filter(listing__user=user)
#   return TemplateResponse(request, 'listings/listings_dashboard.html', {'listings': listings, 'buyers': buyers, 'messages':messages})
