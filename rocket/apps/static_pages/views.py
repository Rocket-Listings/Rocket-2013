from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import cache_page
from django.template.response import TemplateResponse

@cache_control(must_revalidate=True, max_age=3600)
@cache_page(60 * 15)
def http403(request):
    return render(request, 'static_pages/403.html')

@cache_control(must_revalidate=True, max_age=3600)
@cache_page(60 * 15)
def http404(request):
    return render(request, 'static_pages/404.html')

@cache_control(must_revalidate=True, max_age=3600)
@cache_page(60 * 15)
def http500(request):
    return render(request, 'static_pages/500.html')

def home(request):
    if request.user.is_authenticated():
        return redirect('listings.views.dashboard')
    else:
        return what(request)

@cache_control(must_revalidate=True, max_age=3600)
@cache_page(60 * 15)
def homepage(request):
    return TemplateResponse(request, 'static_pages/homepage.html')

@cache_control(must_revalidate=True, max_age=3600)
@cache_page(60 * 15)
def help(request):
    return TemplateResponse(request, 'static_pages/help.html')

@cache_control(must_revalidate=True, max_age=3600)
@cache_page(60 * 15)
def contact(request):
    return TemplateResponse(request, 'static_pages/contact.html')

@cache_control(must_revalidate=True, max_age=3600)
@cache_page(60 * 15)
def faq(request):
    return TemplateResponse(request, 'static_pages/faq.html')

@cache_control(must_revalidate=True, max_age=3600)
@cache_page(60 * 15)
def login(request):
    return TemplateResponse(request, 'rocket_registration/login.html')
