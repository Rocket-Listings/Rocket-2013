from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models import Max

class ListingCategory(models.Model):
	name = models.CharField(max_length = 60)
	description = models.CharField(max_length = 200)

	def __unicode__(self):
		return self.name

class ListingType(models.Model):
	name = models.CharField(max_length = 60)
	description = models.CharField(max_length = 200)

	def __unicode__(self):
		return self.name

class Listing(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField()
	pub_date = models.DateTimeField('date published', auto_now_add=True)
	price = models.IntegerField()
	location = models.CharField(max_length=200)
	category = models.ForeignKey(ListingCategory)
	listing_type = models.ForeignKey(ListingType)
	user = models.ForeignKey(User)
	CL_link = models.URLField(null = True, blank = True)
	

	def max_offer(self):
		"Returns highest offer made by any buyer for that listing"
		return self.offer_set.aggregate(Max('value'))["value__max"]

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('listings.views.detail', args=[str(self.id)])


class ListingSpec(models.Model):
	key = models.CharField(max_length = 60)
	value = models.CharField(max_length = 60)
	listing = models.ForeignKey(Listing)

	def __unicode__(self):
		return self.key + ", " + self.value

class ListingHighlight(models.Model):
	value = models.CharField(max_length = 60)
	listing = models.ForeignKey(Listing)

	def __unicode__(self):
		return self.value

class ListingPhoto(models.Model):
	url = models.CharField(max_length=255)
	upload_date = models.DateTimeField('date uploaded', auto_now_add=True)
	upload_ip = models.IPAddressField()
	order = models.IntegerField(null = True, blank=True)
	listing = models.ForeignKey(Listing, null = True, blank=True)

class Buyer(models.Model):
	listing = models.ForeignKey(Listing, blank=True) 
	name = models.CharField(max_length=255)
	email = models.EmailField(max_length=255, null = True, blank=True)
	def max_offer(self):
		"Returns highest offer the buyer has made for the listing"
		return self.listing.offer_set.filter(buyer=self).aggregate(Max('value'))["value__max"]

	def __unicode__(self):
		return self.name

	def last_message(self):
		"returns the last message between the seller and buyer for that listing"
		return self.listing.message_set.filter(buyer=self).latest('date')


class Offer(models.Model):
	listing = models.ForeignKey(Listing, null = True, blank=True)
	buyer = models.ForeignKey(Buyer)
	value = models.IntegerField()
	date = models.DateTimeField('date offered', auto_now_add=True)
	
class Message(models.Model):
	listing = models.ForeignKey(Listing, null = True, blank=True)
	isSeller = models.NullBooleanField(blank=True)
	buyer = models.ForeignKey(Buyer, null = True, blank=True)
	content = models.TextField()
	date = models.DateTimeField('date received', auto_now_add=True)

















