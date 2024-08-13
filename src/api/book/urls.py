from django.urls import path
from .api import BookList, MyBookList

urlpatterns = [
    path('', BookList.as_view(), name='book-list'),
    path('my/', MyBookList.as_view(), name='my-book-list')
]