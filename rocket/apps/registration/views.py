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

def activate(request,   template_name='registration/activate.html', 
                        success_url='user_info', 
                        extra_context=None, 
                        activation_key=None, **kwargs):

    account = RegistrationProfile.objects.activate_user(activation_key)
    if account:
        # log the user in
        account.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, account)
        # signal activation
        signals.user_activated.send(sender=None, user=account, request=request)
        if success_url is None:
            return redirect('registration_activation_complete');
        else:
            return redirect(success_url)

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name,
                              kwargs,
                              context_instance=context)


def register(request,   success_url=None, 
                        form_class=None, 
                        disallowed_url='registration_disallowed', 
                        template_name='static_pages/index.html',
                        extra_context=None):

    if not getattr(settings, 'REGISTRATION_OPEN', True):
        return redirect(disallowed_url)
    if form_class is None:
        form_class = RegistrationForm
        seller_type = "O"

    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        seller_type = request.POST.get("seller_type", "O")
        if form.is_valid():
            seller_type_field = forms.RegexField(regex=r'^O|D$', max_length=1)
            try:
                seller_type_save = seller_type_field.clean(seller_type)
            except ValidationError as e:
                form._errors["seller_type"] = ErrorList([u"Please choose a valid seller type."])
            else:
                username, email, password = form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password1']
                if Site._meta.installed:
                    site = Site.objects.get_current()
                else:
                    site = RequestSite(request)
                new_user = RegistrationProfile.objects.create_inactive_user(username, email, password, site)
                signals.user_registered.send(sender=None, user=new_user, request=request)

                profile = UserProfile.objects.get(user=new_user)
                profile.seller_type = seller_type_save
                profile.save()
                gravatar_task.delay(new_user, new_user.pk)
                if request.GET.get('next',''):
                    success_url = request.GET.get('next','')
                    return redirect(success_url)
                elif success_url is None:
                    return redirect('registration_complete')
                else:
                    return redirect(success_url)
    else:
        form = form_class()
    
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name, {'form': form, 'seller_type': seller_type}, context_instance=context)