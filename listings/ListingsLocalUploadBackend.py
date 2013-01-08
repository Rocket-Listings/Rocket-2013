from ajaxuploader.backends.thumbnail import ThumbnailUploadBackend
from sorl.thumbnail import get_thumbnail
from django.conf import settings
from listings.models import ListingPhoto, Listing
import uuid

class ListingsLocalUploadBackend(ThumbnailUploadBackend):
	def update_filename(self, request, filename, *args, **kwargs): # override
		"""
		Returns a new name for the file being uploaded.
		Ensure file with name doesn't exist, and if it does,
		create a unique filename to avoid overwriting
		"""
		ext = filename.split('.')[-1]
		return "%s.%s" % (uuid.uuid4(), ext)

	def upload_complete(self, request, filename, *args, **kwargs): # override
		listing_id = int(request.GET['listingid'])
		order = int(request.GET['order'])
		ip = request.META['REMOTE_ADDR']
		listing = None
		url = settings.MEDIA_URL+ self.UPLOAD_DIR + '/' + filename		
		if listing_id != 0:
			listing = Listing.objects.get(id=listing_id)

		photoDict = {	'path': self._path,
						'url': url,
						'upload_ip': ip,
						'order': order,
						'listing': listing }
		photo = ListingPhoto(**photoDict)
		photo.clean()
		photo.save()

		thumbnail = get_thumbnail(self._path, self.DIMENSIONS)
		thumbnail_url = settings.MEDIA_URL + thumbnail.name

		self._dest.close()
		return {'url': url, 'thumbnail_url': thumbnail_url}