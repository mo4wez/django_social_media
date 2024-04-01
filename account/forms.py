from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class UserRegisterationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control',}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control',}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control',}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('Usename exists, try another one.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email exists, Try another one.')
        return email
    
    def clean(self):
        # cleaned data
        cd = super().clean()

        password1 = cd.get('password1')
        password2 = cd.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords does not match.')


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
