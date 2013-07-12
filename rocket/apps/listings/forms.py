from django import forms
from listings.models import Listing, ListingCategory, ListingPhoto
from crispy_forms.helper import FormHelper

class ListingForm(forms.ModelForm):
  class Meta:
    model = Listing
    exclude = ('pub_date', 'user', 'CL_link')

  def __init__(self, *args, **kwargs):
    self.helper = FormHelper()
    super(ListingForm, self).__init__(*args, **kwargs)

class ListingPics(forms.ModelForm):
  class Meta:
    model = ListingPhoto

# category = ChoiceField(map(lambda x: (x.name, x.name), ListingCategory.objects.all()))
# listing_type = ChoiceField(map(lambda x: (x.name, x.name), ListingType.objects.all()))