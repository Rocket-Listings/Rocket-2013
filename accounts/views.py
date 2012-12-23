#from django.contrib.auth import logout
from django.shortcuts import render_to_response #, redirect
#from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
#from django.template import RequestContext

#def login(request):
#	return render_to_response('login.html', {'form': AuthenticationForm() }, context_instance=RequestContext(request))

#def logout(request):
	# Redirect to a success page.

@login_required
def home(request):
	return render_to_response('account_home.html')
