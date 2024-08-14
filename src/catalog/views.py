from datetime import date
import requests
from django.views import View
from django.shortcuts import render, redirect
from auth_app.utils import get_access_token, get_user_from_token
from .models import Book, BorrowedBook


class BaseView(View):

    def get_response(self, url: str, access_token):

        headers = {
            'Authorization': f'Bearer {access_token}'} if access_token else {}

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
    

    def calculate_days_on_hand(self, books):
        today = date.today()
        books_with_days = []

        for item in books:
            borrow_date_str = item.get('borrow_date', '')
            if borrow_date_str:
                borrow_date = date.fromisoformat(borrow_date_str)
            else:
                borrow_date = None

            if borrow_date:
                days_on_hand = (today - borrow_date).days  
            else:
                days_on_hand = 0

            books_with_days.append({
                'book': item.get('book'),
                'borrow_date': borrow_date,
                'days_on_hand': days_on_hand
            })
        
        return books_with_days

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
            books_with_days = self.calculate_days_on_hand(books)             
            print(books_with_days)
            return render(
                request, 
                'catalog/my_books.html', 
                {'books_with_days': books_with_days, 'user': user}
            )
        
        elif response.status_code == 401:
            return render(request, 'catalog/book_catalog.html', {'message': 'Вы не зарегестрированы', 'user': user})


class DebtorsView(MyBookCatalogView):
    

    def get(self, request):
        access_token = get_access_token(self.request)
        user = get_user_from_token(access_token)

        response = self.get_response(
            url='http://localhost:8000/api/books/debtors/',
            access_token=access_token
        )
        data = response.json()

         
        context = {'debtors': data, 'user': user}
        print(context)
        return render(
            request, 
            'catalog/debtors_list.html', 
            context=context
        )

def borrow_book(request, book_id):
    book = Book.objects.get(id=book_id)

    access_token = get_access_token(request)
    user = get_user_from_token(access_token)
    print(user.reader.id, 'borrow_book1111111111111111111')
    borrowed_book = BorrowedBook.objects.create(
        reader=user.reader,
        book=book
    )

    return redirect('my_books')

from django.shortcuts import render, redirect, get_object_or_404
from .models import Book

def return_book(request, book_id):
    access_token = get_access_token(request)
    user = get_user_from_token(access_token)
    
    borrowed_book = BorrowedBook.objects.filter(
        book_id=book_id, 
        reader=user.reader.id
    )
    
    borrowed_book.delete()
    
    return redirect('my_books')