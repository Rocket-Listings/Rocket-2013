from listings.models import ListingCategory
from django.core.cache import cache
from listings.models import ListingCategory, Listing
from django.template.loader import render_to_string
from django.conf import settings
from django.core.cache import cache

def get_cats():
    cache_dict = cache.get_many(['cats'])
    if not cache_dict: # load cats and specs and write to cache
        cats_queryset = ListingCategory.objects.all()
        cat_groups = set(cats_queryset.values_list('group', flat=True))
        cats = {}
        for group in cat_groups:
            cats[group] = list(cats_queryset.filter(group=group))
        cache_dict = {
            # 'cats': cats,
            'cats': cats
        }
        cache.set_many(cache_dict, None) # cache forever
    return cache_dict

def process_autopost_data(listing_id, update=False):
  l = Listing.objects.select_related().get(id=listing_id)
  if l.listing_type == "O":
    cl_type = "fso"
    cl_cat = str(l.category.cl_owner_id)
  else: # Dealer
    cl_type = "fsd"
    cl_cat = str(l.category.cl_dealer_id)

  # specs_set = l.listingspecvalue_set.select_related().all()
  # specs = {}
  # for spec in specs_set:
  #   specs[spec.key.name] = spec.value
  specs = None

  description = render_to_string('listings/cl_description.html', {'description': l.description, 'specs': specs})

  data = {'type': cl_type,
          'cat': cl_cat,
          'market': l.market,
          'sub_market': l.sub_market,
          'hood': l.hood,
          'title': l.title,
          'price': str(l.price),
          'location': l.location,
          'description': description,
          'from': l.user.username + "@" + settings.MAILGUN_SERVER_NAME,
          'photos': map(lambda p: settings.S3_URL + p.key, l.listingphoto_set.all()),
          'pk': l.pk}

  if update:
    data['update_url'] = l.CL_link

  return data
