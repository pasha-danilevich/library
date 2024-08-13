from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, ReaderRegistrationForm, LoginForm
from django.contrib.auth import logout
import requests

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        reader_form = ReaderRegistrationForm(request.POST)
        if user_form.is_valid() and reader_form.is_valid():
            # Создание пользователя
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            
            # Создание читателя
            new_reader = reader_form.save(commit=False)
            new_reader.user = new_user
            new_reader.save()
            
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
        reader_form = ReaderRegistrationForm()
    
    return render(request, 'auth_app/register.html', {'user_form': user_form, 'reader_form': reader_form})

from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, LibrarianRegistrationForm

def register_librarian(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        librarian_form = LibrarianRegistrationForm(request.POST)
        if user_form.is_valid() and librarian_form.is_valid():
            # Создание пользователя
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            
            # Создание библиотекаря
            new_librarian = librarian_form.save(commit=False)
            new_librarian.user = new_user
            new_librarian.save()
            
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
        librarian_form = LibrarianRegistrationForm()
    
    return render(request, 'auth_app/register_librarian.html', {'user_form': user_form, 'librarian_form': librarian_form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Отправка запроса на получение токена
            response = requests.post('http://localhost:8000/jwt/create/', data={
                'username': username,
                'password': password
            })
            if response.status_code == 200:
                tokens = response.json()
                request.session['access'] = tokens['access']
                request.session['refresh'] = tokens['refresh']
                return redirect('catalog') 
            elif response.status_code == 404:
                form.add_error(None, 'Страница не нейдена')
            else:
                form.add_error(None, 'Неверное имя пользователя или пароль.')
    else:
        form = LoginForm()
    
    return render(request, 'auth_app/login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')