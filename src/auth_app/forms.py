from django import forms
from django.contrib.auth.models import User
from .models import Reader, Librarian

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ReaderRegistrationForm(forms.ModelForm):
    class Meta:
        model = Reader
        fields = ['first_name', 'last_name', 'address']


class LibrarianRegistrationForm(forms.ModelForm):
    class Meta:
        model = Librarian
        fields = ['employee_number']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)