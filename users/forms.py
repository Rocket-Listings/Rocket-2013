from django.forms import ModelForm
from users.models import UserProfile

class ListingForm(ModelForm):
	class Meta:
		model = UserProfile
		exclude = ('pub_date','user')

