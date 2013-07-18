from listings.models import ListingCategory, ListingSpecKey
from django.core.cache import cache

def get_listing_vars():
    cache_dict = cache.get_many(['cats', 'spec_keys', 'cat_groups'])
    if not cache_dict: # load cats and specs and write to cache    
      cats = ListingCategory.objects.all()
      cache_dict = {
        'cats': list(cats),
        'spec_keys': list(ListingSpecKey.objects.all()), 
        'cat_groups': map(lambda d: d['group'], cats.values('group').distinct())
      }
      cache.set_many(cache_dict, None) # cache forever
    return cache_dict