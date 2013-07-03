from django.forms import ModelForm
from users.models import UserProfile

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