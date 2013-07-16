from django import forms
from listings.models import Listing, ListingCategory, ListingPhoto
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Fieldset, ButtonHolder, Layout
from crispy_forms.bootstrap import InlineRadios
from listings.widgets import GroupedModelChoiceField

class ListingForm(forms.ModelForm):

  category = GroupedModelChoiceField(ListingCategory.objects.all(), to_field_name='name')
  class Meta:
    model = Listing
    exclude = ('category', 'pub_date', 'user', 'CL_link', 'status')
    widgets = {
      'listing_type': forms.RadioSelect,
    }

  def __init__(self, *args, **kwargs):
    self.helper = FormHelper()
    self.helper.form_tag = False
    self.helper.add_input(Submit('submit', 'Post to Craigslist'))
    self.helper.layout = Layout(
      # 'category',
      Fieldset('Fieldset', 'title', 'price'),
      'description',
      InlineRadios('listing_type'),
      'location'
    )
    super(ListingForm, self).__init__(*args, **kwargs)


class ListingPics(forms.ModelForm):
  class Meta:
    model = ListingPhoto