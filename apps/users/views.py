from listings.models import Listing
#from users.models import UserProfile
from users.forms import UserProfileForm
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
#from forms import UserProfileForm
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail

def overview(request, username=None):
	return info(request, username)

@login_required
def info(request, username=None):
	profile = request.user.get_profile()
	return render(request, 'user_info.html', {'profile':profile,})

@login_required
def edit(request, username):
	if request.user.username == username:
		user = request.user
		profile = user.get_profile()
		if request.method == 'POST':
			user_profile_form = UserProfileForm(request.POST, instance = profile)
			if user_profile_form.is_valid():
				user_profile = user_profile_form.save()
				return redirect(user_profile)
			else:
				return render(request, 'user_edit.html', {'form': user_profile_form})
		else:
			return render(request, 'user_edit.html', {'form': UserProfileForm(instance = profile),})
	else:
		raise PermissionDenied
