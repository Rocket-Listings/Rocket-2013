#We put this file in the users folder but we could put it anywhere we want there

from models import ViewCount

def get_view_count(obj):
	if isinstance(obj, basestring):
		url = obj
	else:
		url = obj.get_absolute_url()

	view_count = ViewCount.objects.get(url=url)
	if view_count:
		return view_count.count
	else:
		return 0

