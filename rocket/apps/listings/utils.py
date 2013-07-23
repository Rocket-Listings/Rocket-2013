from listings.models import ListingCategory, ListingSpecKey
from django.core.cache import cache

def get_listing_vars():
        cache_dict = cache.get_many(['cats', 'spec_keys', 'cat_groups'])
        if not cache_dict: # load cats and specs and write to cache    
            cats_queryset = ListingCategory.objects.all()
            cat_groups = sorted(set(cats_queryset.values_list('group', flat=True)))
            cats = []
            for group in cat_groups:             
                cats_list = sorted(list(cats_queryset.filter(group=group)))
                ordered_cats = []

                step = 6
                if group == 'housing':
                    step = 5

                for i in range(step):
                    ordered_cats += cats_list[i::step]

                cats.append({ 'groupname': group, 'groupcats': ordered_cats })
            cache_dict = {
                'cats': cats,
                'spec_keys': ListingSpecKey.objects.all(),
            }
            cache.set_many(cache_dict, None) # cache forever
        return cache_dict