from ajaxuploader.backends.s3 import S3UploadBackend
from ajaxuploader.backends.local import LocalUploadBackend
from sorl.thumbnail import get_thumbnail
from django.conf import settings
from listings.models import ListingPhoto, Listing
import uuid, os

class RocketUploadBackend(object):
	def update_filename(self, request, filename, *args, **kwargs): # indirectly (through multiple inheritance) overriding AbstractUploadBackend
		ext = filename.split('.')[-1]
		return "%s.%s" % (uuid.uuid4(), ext)

	def upload_complete(self, request, filename, *args, **kwargs): # also overriding
		listing_id = int(request.GET['listingid'])
		order = int(request.GET['order'])
		ip = request.META['REMOTE_ADDR']
		listing = None
#		url = self.UPLOAD_DIR + '/' + filename		
		if listing_id != 0:
			listing = Listing.objects.get(id=listing_id)

		photoDict = {	#'path': self._path,
					#	'url': url,
						'path' : filename,
						'upload_ip': ip,
						'order': order,
						'listing': listing }

		photo = ListingPhoto(**photoDict)
		photo.clean()
		photo.save()

		# path = os.path.join(settings.MEDIA_ROOT, self.UPLOAD_DIR, filename)
		# dims = "100x100"
		# thumbnail = get_thumbnail(path, dims)
		# thumbnail_url = settings.MEDIA_URL + thumbnail.name

		self._dest.close()
		# return {'thumbnail_name': thumbnail.name}

# multiple inheritance for the win! Combining the above class with the DefaultStorageUploadBackend.
class DevelopmentUploadBackend(RocketUploadBackend, LocalUploadBackend): pass


class ProductionUploadBackend(RocketUploadBackend, S3UploadBackend):

	def upload_complete(self, request, filename, *args, **kwargs): # override
		super(S3UploadBackend, self).upload_complete(request, filename, *args, **kwargs)
		return super(RocketUploadBackend, self).upload_complete(request, settings.UPLOAD_DIR+'/'+filename, *args, **kwargs)