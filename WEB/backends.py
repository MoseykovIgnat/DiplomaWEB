from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import *


class PersonalizedLoginBackend(ModelBackend):
    def authenticate(self, request=None, username=None, password=None, **kwars):
        print('HI')
        return None
