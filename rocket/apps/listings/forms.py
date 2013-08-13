from django import forms
from django.forms.models import modelformset_factory
from listings.models import Listing, ListingCategory, ListingPhoto, ListingSpecKey, ListingSpecValue, Message
from listings import utils
from django.forms.models import inlineformset_factory

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        exclude = ('pub_date', 'user', 'CL_link', 'status', 'listing_type')
        widgets = {
            'category': forms.HiddenInput,
            # 'listing_type': forms.HiddenInput  
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

ListingPhotoFormSet = inlineformset_factory(Listing, ListingPhoto, extra=0, can_order=True, can_delete=True, exclude=('order'))

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('date', 'seen')
        fields = ('listing', 'buyer', 'content', 'isSeller')

        def clean(self):
            for field in self.cleaned_data:
                if isinstance(self.cleaned_data[field], basestring):
                    self.cleaned_data[field] = self.cleaned_data[field].strip()
            return self.cleaned_data