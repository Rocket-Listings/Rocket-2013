from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from listings.models import ListingCategory, ListingType
from django.db.models.signals import post_save

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

# Handles user profile creation if not already created
def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
       profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)



#User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])