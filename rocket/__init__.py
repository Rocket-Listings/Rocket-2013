# SITEWIDE UTILITY FUNCTIONS

def get_client_ip(request):
	import os
	from django.conf import settings
	ip_adds = request.environ.get('HTTP_X_FORWARDED_FOR')
	if ip_adds:
		ip_adds = ip_adds.split(",")   
		# print "HTTP_X_FORWARDED_FOR", ip_adds[0]
		return ip_adds[0]
	else:
		print "REMOTE_ADDR", request.META['REMOTE_ADDR']
		return request.META['REMOTE_ADDR']
