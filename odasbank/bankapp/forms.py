from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from .models import User, Transfer, SensitiveData
from django.utils.crypto import get_random_string
import string

class RegistrationForm(UserCreationForm):
    credit_card_number = forms.CharField(max_length=16)
    id_number = forms.CharField(max_length=10)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'credit_card_number', 'id_number']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.balance = 1000
        user.account_number = get_random_string(length=6, allowed_chars=string.digits)
        
        if commit:
            user.save()
            
            SensitiveData.objects.create(
                user=user,
                credit_card_number=self.cleaned_data['credit_card_number'],
                id_number=self.cleaned_data['id_number']
            )
            
        return user
    
class LoginForm(AuthenticationForm):
    pass