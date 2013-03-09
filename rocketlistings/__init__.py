import os
from django.conf import settings

def get_client_ip(request):
	ip_adds = request.environ.get('HTTP_X_FORWARDED_FOR')
	if ip_adds:
		ip_adds = request.environ.get('HTTP_X_FORWARDED_FOR').split(",")   
		return ip_adds[0]
	else:
		return request.META['REMOTE_ADDR']