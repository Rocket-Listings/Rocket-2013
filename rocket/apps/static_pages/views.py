from django.shortcuts import render
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

@cache_control(must_revalidate=True, max_age=3600)
@cache_page(60 * 15)
def what(request):
    return TemplateResponse(request, 'static_pages/what.html')

@cache_control(must_revalidate=True, max_age=3600)
@cache_page(60 * 15)
def how(request):
    return TemplateResponse(request, 'static_pages/how.html')

@cache_control(must_revalidate=True, max_age=3600)
@cache_page(60 * 15)
def why(request):
    return TemplateResponse(request, 'static_pages/why.html')

@cache_control(must_revalidate=True, max_age=3600)
@cache_page(60 * 15)
def pricing(request):
    return TemplateResponse(request, 'static_pages/pricing.html')

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
