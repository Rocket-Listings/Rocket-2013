from listings.models import ListingCategory
from django.core.cache import cache

def get_cats():
    cats = cache.get('cats')
    if not cats: # load cats and specs and write to cache    
        cats_queryset = ListingCategory.objects.all()
        cat_groups = set(cats_queryset.values_list('group', flat=True))
        cats = {}
        for group in cat_groups:
            cats[group] = list(cats_queryset.filter(group=group))
        cache.set('cats', cats, None)
    return cats