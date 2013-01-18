from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings

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

	def __unicode__(self):
		return "%d - %s | %s - %s" % (self.price, self.location, self.title, self.description)

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
	path = models.FilePathField(path=settings.MEDIA_ROOT+'uploads', max_length=255)
	url = models.CharField(max_length=255)
	upload_date = models.DateTimeField('date uploaded', auto_now_add=True)
	upload_ip = models.IPAddressField()
	order = models.IntegerField(null = True, blank=True)
	listing = models.ForeignKey(Listing, null = True, blank=True)
