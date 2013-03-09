StaticStorage = lambda: S3BotoStorage(bucket='static.rocketlistings.com')
MediaStorage  = lambda: S3BotoStorage(bucket='media.rocketlistings.com')