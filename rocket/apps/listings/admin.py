from django.contrib import admin
from listings.models import Listing, Buyer, Offer, Message, ListingPhoto, ListingSpecValue

admin.site.register(Buyer)
admin.site.register(Offer)
admin.site.register(Listing)
admin.site.register(Message)
admin.site.register(ListingPhoto)
admin.site.register(ListingSpecValue)