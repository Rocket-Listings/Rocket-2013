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

class CachedS3BotoStorage(CachedFilesMixin, StaticFilesStorage):
    """
    Backend that makes use of django.contrib.staticfiles' caching mechanism both locally and remotely.
    """
    def __init__(self, *args, **kwargs):
        super(CachedS3BotoStorage, self).__init__(*args, **kwargs)
        kwargs["location"] = "assets"
        self.remote_storage = S3BotoStorage(*args, **kwargs)

    def save(self, name, content):
        name = super(CachedS3BotoStorage, self).save(name, content)
        self.remote_storage._save(name, content)
        return name

    def __save(self, name, content):
        name = super(CachedS3BotoStorage, self)._save(name, content)
        self.remote_storage._save(name, content)
        return name

    def post_process(self, paths, dry_run=False, **options):
        """
        Pulled directly from CachedFilesMixin.

        Modified so that it calls self.__save() instead of self._save(), which should be defined by the class that this is mixed into.
        """
        # don't even dare to process the files if we're in dry run mode
        if dry_run:
            return

        # where to store the new paths
        hashed_paths = {}

        # build a list of adjustable files
        matches = lambda path: matches_patterns(path, self._patterns.keys())
        adjustable_paths = [path for path in paths if matches(path)]

        # then sort the files by the directory level
        path_level = lambda name: len(name.split(os.sep))
        for name in sorted(paths.keys(), key=path_level, reverse=True):

            # use the original, local file, not the copied-but-unprocessed
            # file, which might be somewhere far away, like S3
            storage, path = paths[name]
            with storage.open(path) as original_file:

                # generate the hash with the original content, even for
                # adjustable files.
                hashed_name = self.hashed_name(name, original_file)

                # then get the original's file content..
                if hasattr(original_file, 'seek'):
                    original_file.seek(0)

                hashed_file_exists = self.exists(hashed_name)
                processed = False

                # ..to apply each replacement pattern to the content
                if name in adjustable_paths:
                    content = original_file.read().decode(settings.FILE_CHARSET)
                    for patterns in self._patterns.values():
                        for pattern, template in patterns:
                            converter = self.url_converter(name, template)
                            try:
                                content = pattern.sub(converter, content)
                            except ValueError as exc:
                                yield name, None, exc
                    if hashed_file_exists:
                        self.delete(hashed_name)
                    # then save the processed result
                    content_file = ContentFile(force_bytes(content))
                    saved_name = self.__save(hashed_name, content_file)
                    hashed_name = force_text(saved_name.replace('\\', '/'))
                    processed = True
                else:
                    # or handle the case in which neither processing nor
                    # a change to the original file happened
                    if not hashed_file_exists:
                        processed = True
                        saved_name = self.__save(hashed_name, original_file)
                        hashed_name = force_text(saved_name.replace('\\', '/'))

                # and then set the cache accordingly
                hashed_paths[self.cache_key(name.replace('\\', '/'))] = hashed_name
                yield name, hashed_name, processed

        # Finally set the cache
        self.cache.set_many(hashed_paths)