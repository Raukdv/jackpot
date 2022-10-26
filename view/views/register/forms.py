from django import forms

from core.models import (
    User
)

from core import constants

from django.utils.translation import gettext_lazy as _

from django.contrib.auth import authenticate

class AddressRegisterForm(forms.Form):
    address = forms.CharField()

    address_2 = forms.CharField()

    city = forms.CharField()

    state = forms.CharField()

    zip_code = forms.CharField()

    class Meta:
        fields = ['address','address_2','city', 'zip_code']


class UserRegisterForm(forms.ModelForm):

    email = forms.CharField(required=True, widget = forms.EmailInput(attrs={
        'class':'form-control',
        'id':'email',
        'placeholder': 'Email Address',
        }))
     
    password = forms.CharField(required=True, widget = forms.PasswordInput(attrs={
        'class':'form-control',
        'id':'password',
        'placeholder': 'Password',
        }))

    password2 = forms.CharField(required=True, widget = forms.PasswordInput(attrs={
        'class':'form-control',
        'id':'password2',
        'placeholder': 'Confirme Password',
        }))

    class Meta:
        model = User
        fields = ['email','password', 'password2']
    
    def clean(self):
        cleaned_data = super().clean()
    
        if cleaned_data.get('password2') != cleaned_data.get('password'):
            self.add_error('password', 'Password not match.')

        return cleaned_data

