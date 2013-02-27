from ajaxuploader.backends.s3 import S3UploadBackend
from ajaxuploader.backends.default_storage import DefaultStorageUploadBackend
from sorl.thumbnail import get_thumbnail
from django.conf import settings
from listings.models import ListingPhoto, Listing
import uuid

class RocketUploadBackend(object):

	def upload_complete(self, request, filename, *args, **kwargs): # also overriding
		listing_id = int(request.GET['listingid'])
		order = int(request.GET['order'])
		ip = request.META['REMOTE_ADDR']
		listing = None
		url = self.UPLOAD_DIR + '/' + filename		
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
		return {'path': url, 'thumbnail_path': thumbnail_url}

# multiple inheritance for the win! Combining the above class with the DefaultStorageUploadBackend.
class DevelopmentUploadBackend(RocketUploadBackend, DefaultStorageUploadBackend):
	def update_filename(self, request, filename, *args, **kwargs): # indirectly (through multiple inheritance) overriding AbstractUploadBackend
		ext = filename.split('.')[-1]
		self._path = "%s/%s.%s" % (settings.UPLOAD_DIR, uuid.uuid4(), ext)
		return self.path

class ProductionUploadBackend(RocketUploadBackend, S3UploadBackend):
	def update_filename(self, request, filename, *args, **kwargs): # indirectly (through multiple inheritance) overriding AbstractUploadBackend
		ext = filename.split('.')[-1]
		self._path = "%s%s.%s" % (uuid.uuid4(), ext)
		return self.path

	def upload_complete(self, request, filename, *args, **kwargs): # override
		super(S3UploadBackend, self).upload_complete(request, filename, *args, **kwargs)
		return super(RocketUploadBackend, self).upload_complete(request, filename, *args, **kwargs)