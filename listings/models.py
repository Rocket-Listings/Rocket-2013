from django.db import models
from datetime import datetime

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

class ListingSpec(models.Model):
	key = models.CharField(max_length = 60)
	value = models.CharField(max_length = 60)

	def __unicode__(self):
		return self.key + ", " + self.value

class ListingHighlight(models.Model):
	value = models.CharField(max_length = 60)

	def __unicode__(self):
		return self.value

class Listing(models.Model):
	title = models.CharField(max_length=200)
	description = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
	price = models.IntegerField()
	location = models.CharField(max_length=200)
	category = models.ForeignKey(ListingCategory)
	listing_type = models.ForeignKey(ListingType)
	specs = models.ForeignKey(ListingSpec, blank=True, default=0, null=True)
	highlights = models.ForeignKey(ListingHighlight, blank=True, default=0, null=True)

	def __unicode__(self):
		return "%d - %s | %s - %s" % (self.price, self.location, self.title, self.description)

	def save(self):
		if self.pub_date == None:
			self.pub_date = datetime.now()
			super(Listing, self).save()

