from ajaxuploader.backends.local import LocalUploadBackend
from ajaxuploader.backends.default_storage import DefaultStorageUploadBackend
from sorl.thumbnail import get_thumbnail
from django.conf import settings
from listings.models import ListingPhoto, Listing
import uuid
import os
from rocketlistings import get_client_ip

class RocketUploadBackend(object):
	def update_filename(self, request, filename, *args, **kwargs): # indirectly (through multiple inheritance) overriding AbstractUploadBackend
		ext = filename.split('.')[-1]
		return "%s.%s" % (uuid.uuid4(), ext)

	def upload_complete(self, request, filename, *args, **kwargs): # also overriding
		print "RocketUploadBackend upload_complete"

		listing_id = int(request.GET['listingid'])
		order = int(request.GET['order'])
		ip = get_client_ip(request)
		listing = None
		url = self.UPLOAD_DIR + '/' + filename		

		if listing_id != 0:
			listing = Listing.objects.get(id=listing_id)

		photoDict = {	'url': url,
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

		# self._dest.close()
		# return {'thumbnail_name': thumbnail.name}
		# return {}

# multiple inheritance for the win! Combining the above class with the DefaultStorageUploadBackend.
class DevelopmentUploadBackend(RocketUploadBackend, LocalUploadBackend): pass


class ProductionUploadBackend(RocketUploadBackend, DefaultStorageUploadBackend):

	def upload_complete(self, request, filename, *args, **kwargs): # override
		RocketUploadBackend.upload_complete(self, request, filename, *args, **kwargs)
		return DefaultStorageUploadBackend.upload_complete(self, request, filename, *args, **kwargs)