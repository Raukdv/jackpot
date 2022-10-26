#Views
from django.contrib.auth.views import LoginView, LogoutView

#Tools
from django.contrib import messages
from django.contrib.auth import login

#Redirects
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

#Forms
from . import forms

class LoginView(LoginView):
    form_class = forms.AuthenticationForm
    template_name = 'login/login.html'
    success_url = reverse_lazy('view:home')

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        login(
            self.request,
            form.get_user(),
            backend='django.contrib.auth.backends.ModelBackend'
        )
        
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        url = self.get_redirect_url()
        return url or self.success_url
    
    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)   
        return context