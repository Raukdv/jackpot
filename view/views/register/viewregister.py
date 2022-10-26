#Basesd Views
from django.views.generic import CreateView

#Tools
from django.contrib import messages
from django.contrib.auth import login, authenticate

#Redirects
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.encoding import iri_to_uri

#Forms
from . import forms

#Validator
from . import validators

#Models
from core.models import User

#Exceptions
from django.core.exceptions import SuspiciousOperation

class UserRegisterView(CreateView):
    model = User
    form_class = forms.UserRegisterForm
    success_url = reverse_lazy('view:home')
    template_name = 'register/user_registerview.html'

    def form_valid(self, form):
        #Validate absolute path
        pretender_user_path  = validators.path_user_type_validator(self.request.path)
        user_type = form.cleaned_data['type']

        if pretender_user_path == user_type: #To validate if all the data come from the same place
            if hasattr(form.instance, "type"): #To valide the form still have the attr type
                setattr(form.instance, 'type', user_type)
                user = form.save()
                #Security check complete. Log the user in.
                login(
                    self.request,
                    user,
                )

        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):

        redirect_url = form.cleaned_data.get('referrer') or self.request.META.get('HTTP_REFERER', '')
        if url_has_allowed_host_and_scheme(redirect_url, self.request.get_host()):
            messages.error(self.request, form.errors)
            url = iri_to_uri(redirect_url)
            return HttpResponseRedirect(url)

        # If for some reason someone was manipulated referrer parameter to
        # point to unsafe URL then we will raise Http404 with Suspicious Operation
        raise SuspiciousOperation('Invalid referrer')

    def get_success_url(self): #For some reason HttpResponseRedirect does not work cuz return bytes over get_success_url()
        return reverse_lazy(self.success_url)
    
    def get_context_data(self, **kwargs):
        context = super(UserRegisterView, self).get_context_data(**kwargs)
        
        pretender_user  = validators.path_user_type_validator(self.request.path)

        if pretender_user:
            context['pretender_user'] = pretender_user
        else:
            raise SuspiciousOperation(f'{pretender_user} type value is not allowed')
        return context