from django import forms
from listings.models import Listing, ListingCategory, ListingPhoto
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Fieldset, ButtonHolder, Layout
from crispy_forms.bootstrap import InlineRadios

class ListingForm(forms.ModelForm):
  class Meta:
    model = Listing
    exclude = ('pub_date', 'user', 'CL_link', 'status')
    widgets = {
      'listing_type': forms.RadioSelect,
      'category': forms.HiddenInput
    }

  def __init__(self, *args, **kwargs):
    self.helper = FormHelper()
    self.helper.form_tag = False
    self.helper.add_input(Submit('submit', 'Post to Craigslist'))
    self.helper.layout = Layout(
      Fieldset('Fieldset', 'title', 'price'),
      'description',
      InlineRadios('listing_type'),
      'location'
    )

    super(ListingForm, self).__init__(*args, **kwargs)


class ListingPics(forms.ModelForm):
  class Meta:
    model = ListingPhoto