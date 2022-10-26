#Basesd Views
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

#Tools
from django.contrib import messages

#Redirects
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

#Forms
from . import forms

#Models
from core.models import User

from django.contrib.auth.mixins import LoginRequiredMixin

class UserCreateView(CreateView):
    model = User
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('view:home')
    template_name = 'user/user_createview.html'

    def get_success_url(self): #For some reason HttpResponseRedirect does not work cuz return bytes over get_success_url()
        return reverse_lazy('view:list_user')
 

class UserListView(ListView):
    model = User
    template_name = 'user/user_listview.html'

class UserDetailView(DetailView):
    model = User
    template_name = 'user/user_detailview.html'

    class Meta:
        fields = ('type', 'first_name', 'last_name', 'email',)

class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('view:list_user')
    template_name = 'user/user_comfirmdelete.html'

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'user/user_updateview.html'
    form_class = forms.UserCreateForm