from django.contrib import admin
from listings.models import Listing, Buyer, Offer, SellerMessage, BuyerMessage

admin.site.register(Buyer)
admin.site.register(Offer)
admin.site.register(SellerMessage)
admin.site.register(BuyerMessage)
admin.site.register(Listing)