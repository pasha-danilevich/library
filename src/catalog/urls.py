# catalog/urls.py

from django.urls import path
from .views import BookCatalogView, MyBookCatalogView, DebtorsView, borrow_book

urlpatterns = [
    path('', BookCatalogView.as_view(), name='catalog'),
    path('my-books/', MyBookCatalogView.as_view(), name='my_books'),
    path('borrow/<int:book_id>/', borrow_book, name='borrow_book'),
    path('debtors-list/', DebtorsView.as_view(), name='debtors_list'),
]