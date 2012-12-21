#from django.template.loader import get_template
#from django.template import Context
from django.shortcuts import render_to_response
from django.http import HttpResponse

def home(request):
    return render_to_response('home.html')

