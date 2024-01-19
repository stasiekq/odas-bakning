from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import User, Transfer, SensitiveData
from django.utils.crypto import get_random_string

