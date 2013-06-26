from django.forms import ModelForm, Textarea, ChoiceField
from listings.models import Listing, ListingCategory, ListingType

class ListingForm(ModelForm):
	class Meta:
		model = Listing
		exclude = ('pub_date','user', 'CL_link', 'status')

#	category = ChoiceField(map(lambda x: (x.name, x.name), ListingCategory.objects.all()))
#	listing_type = ChoiceField(map(lambda x: (x.name, x.name), ListingType.objects.all()))