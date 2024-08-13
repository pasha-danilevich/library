from django import forms
from django.contrib.auth.models import User
from .models import Reader, Librarian

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

class ReaderRegistrationForm(forms.ModelForm):
    class Meta:
        model = Reader
        fields = ['address']
        

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)