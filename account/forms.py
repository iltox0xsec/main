from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}), 
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class ChangeUserPasswordForm(PasswordChangeForm):
    old_password = forms.PasswordInput(attrs={'class': 'form-control'})
    new_password1 = forms.PasswordInput(attrs={'class': 'form-control'})
    new_password2 = forms.PasswordInput(attrs={'class': 'form-control'})