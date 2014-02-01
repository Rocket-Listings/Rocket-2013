import hashlib
import random
import re

from django.db import models, IntegrityError
from datetime import datetime
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models import Max
from django.db.models.signals import post_save, pre_save
from django.contrib.sites.models import Site
# from django.forms.util import ValidationError

# Managers!

# Natural key handling for fixtures
# https://docs.djangoproject.com/en/dev/topics/serialization/#natural-keys
class ListingManager(models.Manager):
	def get_by_natural_key(self, title):
		return self.get(title=title)

# Used for both ListingCategory and ListingType and Buyer
class GenericNameManager(models.Manager):
	def get_by_natural_key(self, name):
		return self.get(name=name)

# Listing Categories
class ListingCategory(models.Model):
	objects = GenericNameManager()
	name = models.CharField(max_length = 60)
	cl_owner_id = models.IntegerField(null = True)
	cl_dealer_id = models.IntegerField(null = True)
	description = models.CharField(max_length = 200)
	group = models.CharField(max_length=10, choices=(('forsale', 'For Sale'),('housing', 'Housing')))
	
	def __unicode__(self):
		return self.name

#Listing Status
class ListingStatus(models.Model):
	objects = GenericNameManager()

	name = models.CharField(max_length = 60)
	description = models.CharField(max_length = 200)

	def __unicode__(self):
		return self.name

# Listing
class Listing(models.Model):
	# also for natural key handling
	objects = ListingManager()

	title = models.CharField(max_length=200, null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	price = models.IntegerField(null=True, blank=True)
	location = models.CharField(max_length=200, null=True, blank=True)
	category = models.ForeignKey(ListingCategory, null=True, blank=True)
	listing_type = models.CharField(max_length=1, choices=(('O', 'Owner'),('D', 'Dealer')))
	status = models.ForeignKey(ListingStatus, default=1) # TODO want to be able to listings by this
	
	user = models.ForeignKey(User)

	last_modified = models.DateTimeField(auto_now=True, default=datetime.now, null=True, blank=True)
	create_date = models.DateTimeField(auto_now_add=True, default=datetime.now, null=True, blank=True)		

	CL_link = models.URLField(null=True, blank=True)
	CL_view = models.URLField(null=True, blank=True)
	market = models.CharField(max_length=3, null=True, blank=True)
	sub_market = models.CharField(max_length=3, null=True, blank=True)
	hood = models.CharField(max_length=3, null=True, blank=True)

	class Meta:
		unique_together = ('title', 'user',)

	def max_offer(self):
		"Returns highest offer made by any buyer for that listing"
		return self.offer_set.aggregate(Max('value'))["value__max"]

	def __unicode__(self):
		return u'%s by %s created on %s' % (self.title or str(self.id), self.user.username, self.create_date)

	def get_absolute_url(self):
		return reverse('detail', args=[self.id])

	# need to write this
	def is_valid():
		return True

	#Helper methods for hermes serialization
	def get_verbose_type(self):
		if self.listing_type == u'O':
			return "fso"
		else:
			return "fsd"

	def get_category_id(self):
		if self.listing_type == u'O':
			return self.category.cl_owner_id
		else:
			return self.category.cl_dealer_id

	def get_price_as_string(self):
		return str(self.price)

	def get_photo_urls(self):
		return [photo.url for photo in self.listingphoto_set.all()]

	def get_poll_url(self):
		return "http://" \
			+ str(Site.objects.get_current()) \
			+ reverse('admin_email_poll', args=[self.id]) \
			+ "?format=json"

	def get_view_link_post_url(self):
		return "http://" + str(Site.objects.get_current()) + reverse('view_link_post', args=[self.id])

# pre_save method to clean whitespace preceding a forward slash. See issue #125.
def clean_slash_title(sender, **kwargs):
	listing = kwargs['instance']
	_title = listing.title
	title = re.sub(r'(?<=/) ', '', _title)
	listing.title = title

pre_save.connect(clean_slash_title, sender=Listing)

class Spec(models.Model):
	name = models.CharField(max_length=100)
	value = models.CharField(max_length=100)
	listing = models.ForeignKey(Listing);

	def __unicode__(self):
		return self.name + ' ' + self.value
		
# Listing Photo
class ListingPhoto(models.Model):
	class Meta:
		ordering = ['order',]

	url = models.CharField(max_length=255) # ink url
	key = models.CharField(max_length=255) # s3 path
	order = models.IntegerField(null = True, blank=True)
	listing = models.ForeignKey(Listing, null = True, blank=True)

# Buyer... not associated with account, unique to listing.
class Buyer(models.Model):
	objects = GenericNameManager()
	curMaxOffer = models.IntegerField(null = True, blank = True)
	listing = models.ForeignKey(Listing, blank=True)
	name = models.CharField(max_length=255)
	email = models.EmailField(max_length=255, null = False, blank=False)
	rocket_address = models.CharField(max_length=40, null=True, blank=True)

	def max_offer(self):
		"Returns highest offer the buyer has made for the listing"
		return self.listing.offer_set.filter(buyer=self).aggregate(Max('value'))["value__max"]

	def __unicode__(self):
		return self.name

	def last_message(self):
		"returns the last message between the seller and buyer for that listing"
		return self.listing.message_set.filter(buyer=self).latest('date')

def add_rocket_address(sender, instance, created, **kwargs):
	if created:
		buyer = Buyer.objects.get(pk=instance.id)
		salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
		buyer.rocket_address = hashlib.sha1(salt + buyer.email).hexdigest()
		buyer.save()

post_save.connect(add_rocket_address, sender=Buyer)

# Listing Offer
class Offer(models.Model):
	listing = models.ForeignKey(Listing, null = True, blank=True)
	buyer = models.ForeignKey(Buyer)
	value = models.IntegerField()
	date = models.DateTimeField('date offered', auto_now_add=True, default=datetime.now)

	def __unicode__(self):
		return u'Listing: %s | Amount: $%s' % (self.listing.title, self.value)

# Listing Message
class Message(models.Model):
	listing = models.ForeignKey(Listing, null=True, blank=True)
	isSeller = models.NullBooleanField(blank=False)
	buyer = models.ForeignKey(Buyer, null=True, blank=True)
	content = models.TextField(null=False, blank=False)
	date = models.DateTimeField('date received', auto_now_add=True, default=datetime.now)
	seen = models.NullBooleanField(default=False)

	def __unicode__(self):
		return u'On: %s' % (self.date)
	# def __unicode__(self):
	# 	return u'To: %s %s About: %s From: %s On: %s' % (self.listing.user.first_name, self.listing.user.last_name, self.listing.title, self.buyer.name, self.date)










