from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
UserModel = get_user_model()


class PersonalizedLoginBackend(ModelBackend):
    def authenticate(self, request=None, username=None, password=None, **kwars):
        if UserModel._default_manager.get_by_natural_key(username):
            print('User already exist')
            return None
        else:
            user = User.objects.create_user(username=username, password=password, email='Example@example.com')
            user.save()
            print('User saved')
            return None




