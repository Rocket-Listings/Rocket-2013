from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import cache_page
from django.template.response import TemplateResponse
from users.decorators import attach_client_ip
from mobi.decorators import detect_mobile

# @cache_control(must_revalidate=True, max_age=3600)
# @cache_page(60 * 15)

# @detect_mobile
def home(request):
    # if request.mobile:
    	# print "mobile detected"
    	# return TemplateResponse(request, 'static_pages/index_mobile.html')
    # else:
    if request.user.is_authenticated():
        return redirect('listings.views.dashboard')
    else:
        return index(request)

@attach_client_ip
@cache_control(must_revalidate=True, max_age=3600)
@cache_page(60 * 15)
def index(request):
	return TemplateResponse(request, 'static_pages/index.html', context = {})

def google_webmaster_verification(request):
    return render(request, 'static_pages/googlef43896b8ef9b394c.html')

# Errors
def http403(request):
    return render(request, 'static_pages/403.html')

def http404(request):
    return render(request, 'static_pages/404.html')

def http500(request):
    return render(request, 'static_pages/500.html')

# obscure deactivated pages
# def help(request):
#     return TemplateResponse(request, 'static_pages/help.html')

# def contact(request):
#     return TemplateResponse(request, 'static_pages/contact.html')

# def faq(request):
#     return TemplateResponse(request, 'static_pages/faq.html')
