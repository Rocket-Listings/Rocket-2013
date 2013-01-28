from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from listings.models import ListingCategory, ListingType

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	name = models.CharField(max_length=100, blank=True)
	location = models.CharField(max_length=255, blank=True)
	default_category = models.ForeignKey(ListingCategory, null=True, blank=True)
	default_listing_type = models.ForeignKey(ListingType, null=True, blank=True)
	email = models.EmailField(max_length=255, blank=True)
	bio = models.TextField(blank=True)

	def get_absolute_url(self):
		return reverse('users.views.info', args=[self.user.username])
	
	def __unicode__(self):
		return self.user.username

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])