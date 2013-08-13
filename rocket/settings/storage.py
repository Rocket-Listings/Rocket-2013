# https://github.com/nigma/django-herokuify/blob/master/herokuify/storage.py

from storages.backends.s3boto import S3BotoStorage
# from django.core.files.storage import get_storage_class
from django.contrib.staticfiles.storage import CachedFilesMixin
from django.contrib.staticfiles.storage import StaticFilesStorage

from collections import OrderedDict
import hashlib
import os
import posixpath
import re
try:
    from urllib.parse import unquote, urlsplit, urlunsplit, urldefrag
except ImportError:     # Python 2
    from urllib import unquote
    from urlparse import urlsplit, urlunsplit, urldefrag
from django.conf import settings
from django.core.cache import (get_cache, InvalidCacheBackendError, cache as default_cache)
from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage, get_storage_class
from django.utils.encoding import force_bytes, force_text
from django.utils.functional import LazyObject
from django.utils._os import upath
from django.core.files import File
from django.contrib.staticfiles.utils import check_settings, matches_patterns

# from django.contrib.staticfiles.storage import CachedStaticFilesStorage
# class S3StaticStorage(S3BotoStorage):
#     """
#     Subclasses :class:`storages.backends.s3boto.S3BotoStorage` and
#     sets base location for files to ``/static``.
#     """
#     def __init__(self, *args, **kwargs):
#         kwargs["location"] = "static"
#         super(S3StaticStorage, self).__init__(*args, **kwargs)
class ProductionStaticCachedS3BotoStorage(CachedFilesMixin, S3BotoStorage):
    """
    Backend that makes use of django.contrib.staticfiles' caching mechanism both locally and remotely.
    """
    def __init__(self, *args, **kwargs):
        super(ProductionStaticCachedS3BotoStorage, self).__init__(*args, **kwargs)
        kwargs["location"] = "assets"

class StaticCachedS3BotoStorage(CachedFilesMixin, StaticFilesStorage):
    """
    Backend that makes use of django.contrib.staticfiles' caching mechanism both locally and remotely.
    """
    def __init__(self, *args, **kwargs):
        super(StaticCachedS3BotoStorage, self).__init__(*args, **kwargs)
        kwargs["location"] = "assets"
        self.remote_storage = S3BotoStorage(*args, **kwargs)

    # doesn't save uncached filenames, but also doesn't save compressed files
    def save(self, name, content):
        """
        Saves new content to the file specified by name. The content should be
        a proper File object or any python file-like object, ready to be read
        from the beginning.
        """
        # Get the proper name for the file, as it will actually be saved.
        if name is None:
            name = content.name

        if not hasattr(content, 'chunks'):
            content = File(content)

        name = self.get_available_name(name)
        name = super(StaticCachedS3BotoStorage, self)._save(name, content)

        # Store filenames with forward slashes, even on Windows
        return force_text(name.replace('\\', '/'))

    def _save(self, name, content):
        name = super(StaticCachedS3BotoStorage, self)._save(name, content)
        self.remote_storage._save(name, content)
        return name

class CompressCachedS3BotoStorage(CachedFilesMixin, StaticFilesStorage):
    """
    Backend that makes use of django.contrib.staticfiles' caching mechanism both locally and remotely.
    """
    def __init__(self, *args, **kwargs):
        super(CompressCachedS3BotoStorage, self).__init__(*args, **kwargs)
        kwargs["location"] = "assets"
        self.remote_storage = S3BotoStorage(*args, **kwargs)

    def _save(self, name, content):
        name = super(CompressCachedS3BotoStorage, self)._save(name, content)
        self.remote_storage._save(name, content)
        return name