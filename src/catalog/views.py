from django.views import View
from django.shortcuts import render
import requests
from rest_framework.exceptions import AuthenticationFailed
from auth_app.utils import get_access_token, get_user_from_token

class BookCatalogView(View):
    
    def get(self, request):
        access_token = get_access_token(request)
        user = None

        try:
            user = get_user_from_token(access_token)
        except AuthenticationFailed:
            user = None  

        headers = {'Authorization': f'Bearer {access_token}'} if access_token else {}

        # Запрос к API для получения списка книг
        response = requests.get('http://localhost:8000/api/books/', headers=headers)

        if response.status_code == 200:
            books = response.json()
            return render(request, 'catalog/book_catalog.html', {'books': books, 'user': user})
        else:
            return render(request, 'catalog/book_catalog.html', {'message': 'Книги отсутствуют.', 'user': user})