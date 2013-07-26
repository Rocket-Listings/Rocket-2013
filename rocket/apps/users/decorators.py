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
	def _wrapped_visit_func(request, *args, **kwargs):
		stats = ViewCount.objects.get_or_create(url=request.path)
		stats = stats[0]
		stats.increment()

		return view_func(request, *args, **kwargs)

	return _wrapped_visit_func
