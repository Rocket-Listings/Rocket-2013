from django import forms
from listings.models import Listing, ListingCategory, ListingPhoto, ListingSpecKey, ListingSpecValue
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Fieldset, ButtonHolder, Layout
from crispy_forms.bootstrap import InlineRadios
from listings import utils

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        exclude = ('pub_date', 'user', 'CL_link', 'status')
        widgets = {
            'category': forms.HiddenInput,
            'listing_type': forms.HiddenInput            
        }

class SpecForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SpecForm, self).__init__(*args, **kwargs)
        if args:
            max_length = ListingSpecValue._meta.get_field('value').max_length 
            for name, field in args[0].items():
                if name.find('spec-') != -1:
                    self.fields[name] = forms.CharField(max_length=max_length, required=False)
    # def clean(self):
    #     for name, value in self.cleaned_data.items():
    #         print name, value
    #     return self.cleaned_data

class ListingPics(forms.ModelForm):
    class Meta:
        model = ListingPhoto
