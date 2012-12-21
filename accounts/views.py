from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
from django.contrib.auth.forms import AuthenticationForm

def login(request):
	if request.method == "POST":
		user = AuthenticationForm(request.POST)
		if user.is_valid():
			return redirect('home')
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect('home')
			else:
				pass
				# Return a 'disabled account' error message
		else:
			pass
			# Return an 'invalid login' error message.
	else:
		context = {'form': AuthenticationForm() }
		context.update(csrf(request))
		return render_to_response('login.html', context)



def logout(request):
    logout(request)
    # Redirect to a success page.
