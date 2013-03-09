import os
from django.conf import settings

def get_client_ip(request):
	ip_adds = request.environ.get('HTTP_X_FORWARDED_FOR')
	if ip_adds:
		ip_adds = request.environ.get('HTTP_X_FORWARDED_FOR').split(",")   
		print "IP ADDRESS", ip_adds[0]
		return ip_adds[0]
	else:
		print "IP ADDRESS", ip_adds[0]		
		return request.META['REMOTE_ADDR']