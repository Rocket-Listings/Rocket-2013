from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from listings.models import ListingCategory, ListingType
from django.db.models.signals import post_save
from djangoratings.fields import RatingField
# import django_filepicker

# User Profile
class UserProfile(models.Model):
	SELLER_TYPE_CHOICES = (
		('P', 'Person'),
		('B', 'Business')
	)

	user = models.OneToOneField(User)
	name = models.CharField(max_length=100, blank=True)
	location = models.CharField(max_length=255, blank=True)
	default_category = models.ForeignKey(ListingCategory, null=True, blank=True)
	default_listing_type = models.ForeignKey(ListingType, null=True, blank=True)
	default_seller_type = models.CharField(max_length=1, choices=SELLER_TYPE_CHOICES, default='P')
	phone = models.CharField(max_length=50, blank=True)
	bio = models.TextField(blank=True)
	rating = RatingField(range=3)
	propic = models.CharField(max_length=200, blank=True)
	twitter_handle = models.CharField(max_length=20, blank=True)
	OAUTH_TOKEN = models.CharField(max_length=200, blank=True)
	OAUTH_TOKEN_SECRET = models.CharField(max_length=200, blank=True)

	def get_absolute_url(self):
		return reverse('users.views.info')
		return reverse('users.views.info', args=[self.user.username])

	def __unicode__(self):
		return self.user.username

# Handles user profile creation if not already created
def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
    	profile = UserProfile.objects.create(user=instance)
    	ProfileFB.objects.create(profile=profile)

post_save.connect(create_user_profile, sender=User)


# Model for comments about a user
class UserComment(models.Model): 
	date_posted = models.DateField(auto_now=False, auto_now_add=True)
	comment = models.TextField(blank=False)
	email = models.EmailField(max_length=255, blank=False) # email of commenter
	user = models.ForeignKey(User) # contains user foreignkey
	title = models.CharField(max_length=255, blank=False)
	

	def __unicode__(self):
		return self.user.username


#User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class ProfileFB(models.Model):
	profile = models.OneToOneField(UserProfile)
	username = models.CharField(max_length=50, blank=True)
	name = models.CharField(max_length=100, blank=True)
	link = models.CharField(max_length=100, blank=True)
	picture = models.CharField(max_length=200, blank=True)

	def __unicode__(self):
		return self.username