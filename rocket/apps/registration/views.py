from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.conf import settings
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from users.models import UserProfile
from registration.models import RegistrationProfile
from users.forms import UserProfileForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from registration.forms import RegistrationForm
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django import forms
from django.contrib.auth import login
from registration import signals
from django.forms.util import ErrorList
from registration.tasks import gravatar_task

def activate(request, extra_context=None, activation_key=None, **kwargs):
    account = RegistrationProfile.objects.activate_user(activation_key)
    if account:
        # log the user in
        account.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, account)
        # signal activation
        signals.user_activated.send(sender=None, user=account, request=request)
        return redirect('dashboard')
    else:
        if extra_context is None:
            extra_context = {}
        context = RequestContext(request)
        for key, value in extra_context.items():
            context[key] = callable(value) and value() or value
        return render_to_response('registration/activate.html', kwargs, context_instance=context)


def register(request, extra_context=None):

    if not getattr(settings, 'REGISTRATION_OPEN', True):
        return redirect('registration_disallowed')
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            username, email, password = form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password1']
            site = Site.objects.get_current() if Site._meta.installed else RequestSite(request)
            new_user = RegistrationProfile.objects.create_inactive_user(username, email, password, site)
            signals.user_registered.send(sender=None, user=new_user, request=request)

            profile = UserProfile.objects.get(user=new_user)
            seller_type = form.cleaned_data['seller_type']
            phone = form.cleaned_data['phone']
            profile.seller_type = seller_type
            profile.phone = phone
            profile.save()
            gravatar_task.delay(new_user, new_user.pk)

            success_url = request.GET.get('next','')
            if success_url:                    
                return redirect(success_url)
            else:
                return redirect('registration_complete')
    else:
        form = RegistrationForm()
    
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response('static_pages/index.html', {'register_form': form}, context_instance=context)