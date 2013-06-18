import datetime
from haystack import indexes
from listings.models import Listing

class ListingIndex(indexes.SearchIndex, indexes.Indexable):
	text = CharField(document=True, use_template=True)
	#title = CharField(model_attr='title')
	#description = CharField(model_attr='description')
	pub_date = DateTimeField(model_attr='pub_date')

	def get_model(self):
		return Listing

	def index_queryset(self):
		"""Used when the entire index for model is updated."""
		return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())
