from django import forms

from core.models import (
    User
)

class UserCreateForm(forms.ModelForm):

    first_name = forms.CharField(required=True, widget = forms.TextInput(attrs={
        'class':'form-control',
        'id':'first_name',
        'placeholder': 'First Name',
        }))

    last_name = forms.CharField(required=True, widget = forms.TextInput(attrs={
        'class':'form-control',
        'id':'last_name',
        'placeholder': 'Last Name',
        }))

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

    phone_number = forms.CharField(required=True, widget = forms.TextInput(attrs={
        'class':'form-control',
        'id':'phone_number',
        'placeholder': 'Phone Number',
        }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name','email','password', 'password2', 'phone_number']
    
    def clean(self):
        cleaned_data = super().clean()
    
        if cleaned_data.get('password2') != cleaned_data.get('password'):
            self.add_error('password', 'The password do not match.')

        return cleaned_data
