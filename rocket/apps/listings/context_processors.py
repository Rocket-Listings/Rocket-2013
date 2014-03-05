from django.conf import settings # import the settings file

def s3_url(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'S3_URL': settings.S3_URL}
