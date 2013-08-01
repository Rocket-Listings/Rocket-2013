from models import FirstVisit
from models import ViewCount

def first_visit(view_func): 
    """tests to see if its the first time has visited a page

    to use this functionality, set request.user.is_owner to a boolean. Need to check if the user is logged to do that
"""
    def _wrapped_visit_func(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        
        if request.user.is_authenticated() and hasattr(request.user,'is_owner') and request.user.is_owner and hasattr(response,'template_name'):
            if not FirstVisit.objects.filter(user=request.user.id, template_path=response.template_name).exists():
                response.context_data.update({'first_visit': True})
                FirstVisit.objects.create(user=request.user, template_path=response.template_name)
        
        return response

    return _wrapped_visit_func


def view_count(view_func):
    """keeps track of the number of views a page gets
    
    view_count function is used to keep track of the number of times an anonymous or a non-owner of a page 
    views a certain page of another user. It will not add to the page views if the owner of the page visits the page.
    To use this functionality, you need to set the property of request.user.is_owner to a boolean. 
    The way it has been done is that if request.user is equal to the owner of the page being visited skip_count is set to True
    otherwise it is set to false. Check also if the user is logged in with a request.user.is_authenticated().
    Also the decorator needs to be called at the beginning of the function.
    """
    def _wrapped_visit_func(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
                
        if not (hasattr(request.user,'is_owner') and request.user.is_owner):
            view_count = ViewCount.objects.get_or_create(url=request.path)[0]
            view_count.increment()

        return response

    return _wrapped_visit_func

