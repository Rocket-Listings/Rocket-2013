from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from listings.models import ListingCategory, ListingType

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	name = models.CharField(max_length=100)
	location = models.CharField(max_length=255)
	default_category = models.ForeignKey(ListingCategory)
	default_listing_type = models.ForeignKey(ListingType)
	email = models.EmailField(max_length=255)
	bio = models.TextField()
	
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
