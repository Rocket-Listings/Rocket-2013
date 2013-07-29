from models import FirstVisit
from models import ViewCount

def first_visit(view_func):	
	def _wrapped_visit_func(request, *args, **kwargs):
		response = view_func(request, *args, **kwargs)
 		
 		if hasattr(response,'template_name'):
			if not FirstVisit.objects.filter(user=request.user.id, template_path=response.template_name).exists():
				response.context_data.update({'first_visit': True})
				FirstVisit.objects.create(user=request.user, template_path=response.template_name)
		
		return response

	return _wrapped_visit_func


def view_count(view_func):
	"""keeps track of the number of views a page gets
	
	view_count function is used to keep track of the number of times an anonymous or a non-owner of a page 
views a certain page of another user. It will not add to the page views if the owner of the page visits the page.
To use this functionality, you need to include set the property of request.user.skip_count to a boolean. 
The way it has been done is that if request.user is equal to the owner of the page being visited skip_count is set to True
otherwise it is set to false. Also the decorator needs to be called at the beginning of the function.
"""
	def _wrapped_visit_func(request, *args, **kwargs):
		response = view_func(request, *args, **kwargs)
		
		stats = ViewCount.objects.get_or_create(url=request.path)[0]
		
		if not (hasattr(request.user,'skip_count') and request.user.skip_count):
			stats.increment()

		return response

	return _wrapped_visit_func

