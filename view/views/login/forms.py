from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import authenticate

class AuthenticationForm(auth_forms.AuthenticationForm):

    username = forms.CharField(label='Email', required=False, widget = forms.EmailInput(attrs={
        'class':'form-control',
        'id':'exampleInputEmail1',
        'aria-describedby':"emailHelp",
        'placeholder': 'Email Address',
        }))
    
    password = forms.CharField(label='Password', required=False, widget = forms.PasswordInput(attrs={
        'class':'form-control',
        'id':'exampleInputPassword1',
        'placeholder': 'Password',
        }))

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        self.user_cache = authenticate(
                self.request, 
                username=username, 
                password=password
            )

        if self.user_cache is None:
            raise self.get_invalid_login_error()
        else:
            self.confirm_login_allowed(self.user_cache)


        return cleaned_data