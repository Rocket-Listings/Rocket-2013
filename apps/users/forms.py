from django.forms import ModelForm
from users.models import UserProfile, UserComment, User
from django.forms.models import inlineformset_factory
from django import forms

class UserProfileForm(ModelForm):
	class Meta:
		model = UserProfile
		exclude = ('user')
		fields = ('name', 'email', 'phone', 'location', 'bio', 'default_category', 'default_listing_type', 'nameprivate', 'locationprivate', 'propic')

	def clean(self):
		for field in self.cleaned_data:
			if isinstance(self.cleaned_data[field], basestring):
				self.cleaned_data[field] = self.cleaned_data[field].strip()
		return self.cleaned_data

class CommentSubmitForm(ModelForm):
	class Meta:
		model = UserComment
		fields = ('name','email','comment', 'title')	
		exclude = ('user', 'is_removed', 'date_posted')

	def clean(self):
		for field in self.cleaned_data:
			if isinstance(self.cleaned_data[field], basestring):
				self.cleaned_data[field] = self.cleaned_data[field].strip()
		return self.cleaned_data
