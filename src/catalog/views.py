from django.views import View
from django.shortcuts import render
import requests
from rest_framework.exceptions import AuthenticationFailed
from auth_app.utils import get_access_token, get_user_from_token

class BaseView(View):
    
    def get_response(self, url: str, access_token):

        headers = {'Authorization': f'Bearer {access_token}'} if access_token else {}

        # Запрос к API для получения списка книг
        response = requests.get(url, headers=headers)
        
        return response

class BookCatalogView(BaseView):
    
    def get(self, request):
        access_token = get_access_token(request)
        user = get_user_from_token(access_token)
        
        
        response = self.get_response(
            url='http://localhost:8000/api/books/', 
            access_token=access_token
        )

        if response.status_code == 200:
            books = response.json()
            return render(request, 'catalog/book_catalog.html', {'books': books, 'user': user})
        else:
            return render(request, 'catalog/book_catalog.html', {'message': 'Книги отсутствуют.', 'user': user})
        
        

class MyBookCatalogView(BaseView):
    
    def get(self, request):
        access_token = get_access_token(request)
        user = get_user_from_token(access_token)

        response = self.get_response(
            url='http://localhost:8000/api/books/my/', 
            access_token=access_token
        )

        if response.status_code == 200:
            books = response.json()
            print(books)
            return render(request, 'catalog/my_books.html', {'books': books, 'user': user})
        elif response.status_code == 401:
            return render(request, 'catalog/book_catalog.html', {'message': 'Вы не зарегестрированы', 'user': user})

class DebtorsView(BaseView):
    
    def get(self, request):
        access_token = get_access_token(self.request)
        user = get_user_from_token(access_token)
        
        response = self.get_response(
            url='http://localhost:8000/api/books/', 
            access_token=access_token
        )
        debtors = response.json()
        return render(request, 'catalog/debtors_list.html', {'debtors': debtors, 'user': user})

