from listings.models import Listing
#from users.models import UserProfile
from users.forms import UserProfileForm
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
#from forms import UserProfileForm
from django.core.exceptions import PermissionDenied

@login_required
def overview(request, username=None):
	user = request.user
	if username:
		user = get_object_or_404(User, username=username)
	listings = Listing.objects.filter(user=user).order_by('-pub_date')[:10]
# 	userprofile = request.user.userprofile # if no username parameter is passed, defaults to the currently logged in user.
# 	if request.user.username == username: # updating his own listing
# 		if request.method == 'POST':
# 			pass
# #			userprofile_form = UserProfileForm(request.POST, instance = userprofile)
# #			if userprofile_form.is_valid():
# #				return redirect(request.user)
# 			#else:
# #				return render(request, 'user_update.html', {'form': listing_form})
# 		else:
# 			return render(request, 'listing_update.html', {'form':ListingForm(instance = listing),})
# 	else:
# 		return render(request, '403.html')
	
	return render(request, 'user_overview.html', {'listings': listings})

@login_required
def listings(request, username):
	user = request.user # if no username parameter is passed, defaults to the currently logged in user.
	if username:
		user = get_object_or_404(User, username=username)
	listings = Listing.objects.filter(user=user).order_by('-pub_date')[:10]
	return render(request, 'user_overview.html', {'listings': listings})

@login_required
def info(request, username):
	profile = request.user.profile
	return render(request, 'user_info.html', {'profile':profile,})

@login_required
def edit(request, username):
	if request.user.username == username:
		user = request.user
		profile = user.profile
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
