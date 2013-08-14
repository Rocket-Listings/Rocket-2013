from django.forms import ModelForm
from users.models import UserProfile, UserComment, User
from django.forms.models import inlineformset_factory
from django import forms
from django.contrib.auth.models import User
from django.forms.util import ErrorList
from django.core.validators import validate_email



class UserProfileForm(ModelForm):
	email = forms.EmailField(max_length=75, required=True)
	class Meta:
		model = UserProfile
		exclude = ('user', 'twitter_handle', 'TWITTER_OAUTH_TOKEN', 'TWITTER_OAUTH_TOKEN_SECRET','listing_credits')
		fields = ('name', 'phone', 'location', 'bio', 'default_category', 'seller_type', 'propic')

	def clean(self):
		for field in self.cleaned_data:
			if isinstance(self.cleaned_data[field], basestring):
				self.cleaned_data[field] = self.cleaned_data[field].strip()
		return self.cleaned_data

class CommentSubmitForm(ModelForm):
	class Meta:
		model = UserComment
		fields = ('email','comment', 'title', 'rating')
		exclude = ('user', 'date_posted')

	def clean(self):
		for field in self.cleaned_data:
			if isinstance(self.cleaned_data[field], basestring):
				self.cleaned_data[field] = self.cleaned_data[field].strip()
		return self.cleaned_data

