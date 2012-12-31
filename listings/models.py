from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

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
	description = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
	price = models.IntegerField()
	location = models.CharField(max_length=200)
	category = models.ForeignKey(ListingCategory)
	listing_type = models.ForeignKey(ListingType)
	user = models.ForeignKey(User)

	def __unicode__(self):
		return "%d - %s | %s - %s" % (self.price, self.location, self.title, self.description)

	def save(self):
		if self.pub_date == None:
			self.pub_date = datetime.now()
			super(Listing, self).save()

	def get_absolute_url(self):
		return reverse('listings.views.read', args=[str(self.id)])

class ListingSpec(models.Model):
	key = models.CharField(max_length = 60)
	value = models.CharField(max_length = 60)
	listing = models.ForeignKey(Listing, default = Listing.objects.all()[0])

	def __unicode__(self):
		return self.key + ", " + self.value

class ListingHighlight(models.Model):
	value = models.CharField(max_length = 60)
	listing = models.ForeignKey(Listing, default = Listing.objects.all()[0])

	def __unicode__(self):
		return self.value