import requests
from datetime import date

from django.urls import reverse
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site

from auth_app.utils import get_access_token, get_user_from_token
from .models import Book, BorrowedBook


class BaseView(View):

    def get_response(self, url: str, access_token):
        headers = {
            'Authorization': f'Bearer {access_token}'} if access_token else {}
        response = requests.get(url, headers=headers)

        return response

    def get_full_url(self, uri: str) -> str:
        host = get_current_site(self.request).domain
        full_url = f'http://{host}{uri}'
        return full_url


class BookCatalogView(BaseView):

    def get(self, request):
        access_token = get_access_token(request)
        user = get_user_from_token(access_token)
        uri = reverse('book-list')

        response = self.get_response(
            url=self.get_full_url(uri),
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
        uri = reverse('my-book-list')

        response = self.get_response(
            url=self.get_full_url(uri),
            access_token=access_token
        )

        if response.status_code == 200:
            books = response.json()

            books_with_days = self.calculate_days_on_hand(books)

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
        uri = reverse('debtors-list')

        response = self.get_response(
            url=self.get_full_url(uri),
            access_token=access_token
        )

        data = response.json()

        context = {'debtors': data, 'user': user}

        return render(
            request,
            'catalog/debtors_list.html',
            context=context
        )


def borrow_book(request, book_id):
    book = Book.objects.get(id=book_id)

    access_token = get_access_token(request)
    user = get_user_from_token(access_token)

    borrowed_book = BorrowedBook.objects.create(
        reader=user.reader,
        book=book
    )

    return redirect('my_books')


def return_book(request, book_id):
    access_token = get_access_token(request)
    user = get_user_from_token(access_token)

    borrowed_book = BorrowedBook.objects.filter(
        book_id=book_id,
        reader=user.reader.id
    )

    borrowed_book.delete()

    return redirect('my_books')
