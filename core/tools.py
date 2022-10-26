from django.shortcuts import get_object_or_404
from core.models import User
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
import string
import random

#Simple tool for return user object by id
def get_user_object(pk=None):  
    user = None
    if pk:
        user = get_object_or_404(User, pk=pk)
    
    return user

#Simple tool for return user object by any field - in development
def get_dinamic_user(*args, **kwargs):
    try:
        return User.objects.get(email=kwargs.get('email', None))
    except ObjectDoesNotExist:
        return None

#Simple tool to generate a random password

def random_password():
    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
    random.shuffle(characters)
    password = []
    for i in range(20):
        password.append(random.choice(characters))
    random.shuffle(password)
    passw = "".join(password)
    return passw



    

