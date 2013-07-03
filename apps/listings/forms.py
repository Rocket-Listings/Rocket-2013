from django.forms import ModelForm, Textarea, ChoiceField
from listings.models import Listing, ListingCategory, ListingType, ListingPhoto

class ListingForm(ModelForm):
	class Meta:
		model = Listing
		exclude = ('pub_date','user', 'CL_link', 'status')

class ListingPics(ModelForm):
	class Meta:
		model = ListingPhoto

#	category = ChoiceField(map(lambda x: (x.name, x.name), ListingCategory.objects.all()))
#	listing_type = ChoiceField(map(lambda x: (x.name, x.name), ListingType.objects.all()))