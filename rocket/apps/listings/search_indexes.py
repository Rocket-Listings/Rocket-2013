import datetime
from haystack import indexes
from listings.models import Listing

class ListingIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	title = indexes.CharField(model_attr='title')
	description = indexes.CharField(model_attr='description')
	last_modified = indexes.DateTimeField(model_attr='last_modified')
	url_id = indexes.CharField(model_attr='id')
	category = indexes.CharField(model_attr='category')
	identification = indexes.CharField(model_attr='id')
	price = indexes.IntegerField(model_attr='price')
	content_auto = indexes.NgramField(model_attr='title')
	user = indexes.CharField(model_attr='user')

	def get_model(self):
		return Listing

	def index_queryset(self, **kwargs):
		"""Used when the entire index for model is updated."""
		return self.get_model().objects.filter(last_modified__lte=datetime.datetime.now())
