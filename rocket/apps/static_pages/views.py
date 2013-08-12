from django.shortcuts import render

def http403(request):
    return render(request, 'static_pages/403.html')

def http404(request):
    return render(request, 'static_pages/404.html')

def http500(request):
    return render(request, 'static_pages/500.html')