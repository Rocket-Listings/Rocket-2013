import requests
import re
import json
from django.conf import settings
from users.models import FirstVisit

def First_Visit(func):	
	if not FirstVisit.objects.filter(user=request.user.id, url=request.path).exists():
		first_visit = 1
		FirstVisit(user=request.user, url=request.path).save()
	else:
		first_visit = 0

	return func(request,first_visit)
