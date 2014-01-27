from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from listings.models import ListingCategory
from django.db.models.signals import post_save
from django.conf import settings

# import django_filepicker

# User Profile
class UserProfile(models.Model):
	user = models.OneToOneField(User)

	name = models.CharField(max_length=100, blank=True)
	location = models.CharField(max_length=255, blank=True)
	default_category = models.ForeignKey(ListingCategory, null=True, blank=True)
	seller_type = models.CharField(max_length=1, choices=(('O', 'Owner'),('D', 'Dealer')), null=False, blank=False)
	phone = models.CharField(max_length=50, null=False, blank=False)
	bio = models.TextField(blank=True)
	propic = models.CharField(max_length=200, blank=True)

	fbProfile = models.OneToOneField('ProfileFB', null=True, blank=True)
	twitter_handle = models.CharField(max_length=20, blank=True)
	TWITTER_OAUTH_TOKEN = models.CharField(max_length=200, blank=True)
	TWITTER_OAUTH_TOKEN_SECRET = models.CharField(max_length=200, blank=True)

	listing_credits = models.IntegerField(default=999)
	total_credits = models.IntegerField(default=999)

	profile_completed_once = models.BooleanField(default=False)
	twitter_connected_once = models.BooleanField(default=False)
	facebook_connected_once = models.BooleanField(default=False)

	def get_absolute_url(self):
		return reverse('users.views.profile', args=[self.user])

	def get_display_name(self):
		if self.name:
			return self.name
		return self.user.username

	def __unicode__(self):
		return self.user.username

	def add_credit(self, add=1):
		self.listing_credits += add
		self.total_credits += add
		self.save()

	def subtract_credit(self, subtract=1):
		self.listing_credits -= subtract
		self.save()

	def filled_out(self):
		return all([self.name, self.location, self.phone, self.bio, self.propic, self.seller_type])

	#Helper methods for hermes serialization
	def get_rocket_email(self):
		return self.user.username + "@" + settings.MAILGUN_SERVER_NAME
	def get_user_pn(self):
		return self.phone

# Handles user profile creation if not already created
def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
    	profile = UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


# Model for comments about a user
class UserComment(models.Model): 
	date_posted = models.DateField(auto_now=False, auto_now_add=True)
	comment = models.TextField(blank=False)
	email = models.EmailField(max_length=255, blank=False) # email of commenter
	user = models.ForeignKey(User) # contains user foreignkey
	title = models.CharField(max_length=255, blank=False)
	rating = models.IntegerField(blank=False, default="5")
	

	def __unicode__(self):
		return self.user.username


#User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class ProfileFB(models.Model):
	username = models.CharField(max_length=50, blank=True)
	name = models.CharField(max_length=100, blank=True)
	link = models.CharField(max_length=100, blank=True)
	picture = models.CharField(max_length=200, blank=True)

	def __unicode__(self):
		return self.username

class FirstVisit(models.Model):
	template_path = models.CharField(max_length=100, blank=True)
	user = models.ForeignKey('auth.User')


class ViewCount(models.Model):
	url = models.URLField()
	count = models.IntegerField(default=0)

	def increment(self):
		self.count += 1
		self.save()


