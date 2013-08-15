import hashlib
import random

from django.db import models, IntegrityError
from datetime import datetime
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models import Max
from django.db.models.signals import post_save
from django.forms.util import ValidationError

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
	title = models.CharField(max_length=200)
	description = models.TextField()
	pub_date = models.DateTimeField('date published', auto_now_add=True, default=datetime.now)
	listing_type = models.CharField(max_length=1, choices=(('O', 'Owner'),('D', 'Dealer')))
	price = models.IntegerField()
	location = models.CharField(max_length=200)
	category = models.ForeignKey(ListingCategory)
	status = models.ForeignKey(ListingStatus, null = True, default=1) # TODO want to be able to listings by this
	user = models.ForeignKey(User)
	CL_link = models.URLField(null=True, blank=True)

	class Meta:
		unique_together = ('title', 'user',)

	def max_offer(self):
		"Returns highest offer made by any buyer for that listing"
		return self.offer_set.aggregate(Max('value'))["value__max"]

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('detail', args=[self.id])

	def get_view_count(self):
		from users.models import ViewCount
		return ViewCount.objects.get_or_create(url=self.get_absolute_url())[0].count

# Listing Specification
class ListingSpecKey(models.Model):
	name = models.CharField(max_length = 100)
	category = models.ForeignKey(ListingCategory)

	def __unicode__(self):
		return self.name

class ListingSpecValue(models.Model):
	value = models.CharField(max_length = 100)
	key = models.ForeignKey(ListingSpecKey)
	listing = models.ForeignKey(Listing)

	def __unicode__(self):
		return self.value
		
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
		return "$ " + str(self.value)

# Listing Message
class Message(models.Model):
	listing = models.ForeignKey(Listing, null=False, blank=False)
	isSeller = models.NullBooleanField(blank=False)
	buyer = models.ForeignKey(Buyer, null=False, blank=False)
	content = models.TextField(null=False, blank=False)
	date = models.DateTimeField('date received', auto_now_add=True, default=datetime.now)
	seen = models.NullBooleanField(default=False)
