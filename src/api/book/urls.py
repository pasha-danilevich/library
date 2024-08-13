from django.urls import path
from .api import BookList

urlpatterns = [
    path('', BookList.as_view(), name='book-list'),
]