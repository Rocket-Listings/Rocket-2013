from django import forms
from listings.models import Listing, ListingCategory, ListingPhoto
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Fieldset, ButtonHolder, Layout
from crispy_forms.bootstrap import InlineRadios


class ListingForm(forms.ModelForm):
  class Meta:
    model = Listing
    exclude = ('pub_date', 'category', 'user', 'CL_link', 'status')
    widgets = {
      'listing_type': forms.RadioSelect
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


class CategorySelectWidget(forms.widgets.Widget): # Straight ripping off forms.widgets.Select
  allow_multiple_selected = False

  def __init__(self, attrs=None, choices=(), groups=()):
    super(Select, self).__init__(attrs)
    # choices can be any iterable, but we may need to render this widget
    # multiple times. Thus, collapse it into a list so it can be consumed
    # more than once.
    self.groups = list(groups)
    self.choices = list(choices)

  def render(self, name, value, attrs=None, choices=()):
    if value is None: value = ''
    final_attrs = self.build_attrs(attrs, name=name)
    output = '<input id="cat-input" type="hidden" name="cat"><ul class="nav nav-tabs">'
    output = [format_html('<select{0}>', flatatt(final_attrs))]
    options = self.render_options(choices, [value])
    if options:
      output.append(options)
    output.append('</select>')
    return mark_safe('\n'.join(output))

  def render_option(self, selected_choices, option_value, option_label):
      option_value = force_text(option_value)
      if option_value in selected_choices:
        selected_html = mark_safe(' selected="selected"')
        if not self.allow_multiple_selected:
          # Only allow for a single selection.
          selected_choices.remove(option_value)
      else:
        selected_html = ''
      return format_html('<option value="{0}"{1}>{2}</option>',
                         option_value,
                         selected_html,
                         force_text(option_label))

  def render_options(self, choices, selected_choices):
    # Normalize to strings.
    selected_choices = set(force_text(v) for v in selected_choices)
    output = []
    for option_value, option_label in chain(self.choices, choices):
      if isinstance(option_label, (list, tuple)):
        output.append(format_html('<optgroup label="{0}">', force_text(option_value)))
        for option in option_label:
          output.append(self.render_option(selected_choices, *option))
        output.append('</optgroup>')
      else:
        output.append(self.render_option(selected_choices, option_value, option_label))
  return '\n'.join(output)


