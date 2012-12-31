from ajaxuploader.backends.thumbnail import ThumbnailUploadBackend
import os
from django.conf import settings
import uuid

class ListingsLocalUploadBackend(ThumbnailUploadBackend):
	def upload_complete(self, request, filename, *args, **kwargs): # override
		path = settings.MEDIA_URL + self.UPLOAD_DIR + "/" + filename
		self._dest.close()
		return {"path": path}

	def update_filename(self, request, filename, *args, **kwargs): # override
		"""
		Returns a new name for the file being uploaded.
		Ensure file with name doesn't exist, and if it does,
		create a unique filename to avoid overwriting
		"""
		ext = filename.split('.')[-1] 
		filename = "%s.%s" % (uuid.uuid4(), ext)
		return os.path.join(settings.MEDIA_ROOT, self.UPLOAD_DIR, filename)