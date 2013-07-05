from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from listings.models import ListingCategory, ListingType
from django.db.models.signals import post_save
# import django_filepicker

# User Profile
class UserProfile(models.Model):
	user = models.OneToOneField(User)
	name = models.CharField(max_length=100, blank=True)
	location = models.CharField(max_length=255, blank=True)
	default_category = models.ForeignKey(ListingCategory, null=True, blank=True)
	default_listing_type = models.ForeignKey(ListingType, null=True, blank=True)
	email = models.EmailField(max_length=255, blank=False)
	phone = models.CharField(max_length=50, blank=True)
	bio = models.TextField(blank=True)
	nameprivate = models.BooleanField(blank=False, null=False)
	locationprivate = models.BooleanField(blank=False, null=False)
	propic = models.CharField(max_length=200, blank=True)

	#photo = django_filepicker.models.FPFileField(upload_to='uploads')

	def get_absolute_url(self):
		return reverse('users.views.info')
		return reverse('users.views.info', args=[self.user.username])
	
	def __unicode__(self):
		return self.user.username


# Handles user profile creation if not already created
def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
    	UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


# Model for comments about a user
class UserComment(models.Model): 
	date_posted = models.DateField(auto_now=False, auto_now_add=False)
	comment = models.TextField()
	email = models.EmailField() # email of commenter
	user = models.ForeignKey(User) # contains user foreignkey
	is_removed = models.BooleanField() # if true comment will not display
	name = models.CharField(max_length=15)

	def __unicode__(self):
		return self.user.username
 

#User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])