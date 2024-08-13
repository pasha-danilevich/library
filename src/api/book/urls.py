from django.urls import path
from .api import *

urlpatterns = [
    path('', BookList.as_view(), name='book-list'),
    path('my/', MyBookList.as_view(), name='my-book-list'),
    path('debtors/', DebtorList.as_view(), name='my-book-list'),
]